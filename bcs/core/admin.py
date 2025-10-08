from importlib import import_module
import sys

from django.contrib import admin
from django.contrib.admin.utils import quote
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.db import models
from django.forms import Textarea
from polymorphic.models import PolymorphicModel

from core.apps import get_calling_app_config


def get_admin_form_url(instance):
    content_type = ContentType.objects.get_for_model(instance)
    app_label = content_type.app_label

    admin_url = reverse(
        viewname=f"admin:{app_label}_{content_type.model}_change",
        args=(quote(instance.pk),),
    )

    return admin_url


def get_pk_from_admin_url(url):
    """Takes admin change form URL and extracts object's pk"""
    words = url.split("/")
    return int(words[-3])


def is_polymorphic_parent(model):
    if not issubclass(model, PolymorphicModel):
        return False
    # Check if any direct subclass is polymorphic (a child model)
    for subclass in model.__subclasses__():
        if issubclass(subclass, PolymorphicModel):
            return True
    return False


class UsedOnlyFKFilter(admin.RelatedFieldListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        # Determine which FK values are actually used
        used_ids = model.objects.values_list(field.name, flat=True).distinct()

        # Limit the field's queryset before calling the parent init
        self._original_limit_choices_to = field.remote_field.limit_choices_to
        field.remote_field.limit_choices_to = {"pk__in": used_ids}

        super().__init__(
            field=field,
            request=request,
            params=params,
            model=model,
            model_admin=model_admin,
            field_path=field_path,
        )

        # Restore original limit_choices_to in case it's reused elsewhere
        field.remote_field.limit_choices_to = self._original_limit_choices_to


def get_used_m2m_ids(model, m2m_field_name):
    field = model._meta.get_field(m2m_field_name)

    through_model = field.remote_field.through
    target_model = field.remote_field.model

    # Find FK field name in through model pointing to target model
    for f in through_model._meta.fields:
        if (
            f.is_relation
            and f.remote_field
            and f.remote_field.model == target_model
        ):
            target_fk_name = f.name
            break
    else:
        raise RuntimeError(
            "Could not determine foreign key to related model in through table."
        )

    return through_model.objects.values_list(
        target_fk_name, flat=True
    ).distinct()


class UsedOnlyM2MFilter(admin.RelatedFieldListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        used_ids = get_used_m2m_ids(model=model, m2m_field_name=field.name)
        # Limit the choices shown in the filter dropdown
        self._original_limit_choices_to = field.remote_field.limit_choices_to
        field.remote_field.limit_choices_to = {"pk__in": used_ids}

        super().__init__(
            field=field,
            request=request,
            params=params,
            model=model,
            model_admin=model_admin,
            field_path=field_path,
        )

        # Restore original
        field.remote_field.limit_choices_to = self._original_limit_choices_to


class BaseModelAdmin(admin.ModelAdmin):

    actions = ["save_selected"]
    list_filter_exclude = set()
    hide_from_index = False
    hide_base_class_from_index = True
    save_as = True

    def save_selected(self, request, queryset):
        pass

    save_selected.short_description = "Save selected objects"

    def _get_list_filter(self):
        exclude = getattr(self, "list_filter_exclude", set())

        if exclude == "__all__":
            return []

        list_filter = list(self.list_filter)
        if not list_filter:
            for field in self.model._meta.get_fields():
                if field.name not in exclude and (
                    getattr(field, "choices", None)
                    or isinstance(
                        field, (models.BooleanField, models.ForeignKey)
                    )
                ):
                    list_filter.append(field.name)

        return list_filter

    def smart_wrap_filters(self, list_filter):
        filters = list_filter
        smart_filters = []

        for f in filters:
            if isinstance(f, tuple):
                # Already a custom filter
                smart_filters.append(f)
            elif isinstance(f, str):
                field = self.model._meta.get_field(f)

                if isinstance(field, models.ForeignKey):
                    smart_filters.append((f, UsedOnlyFKFilter))
                elif isinstance(field, models.ManyToManyField):
                    smart_filters.append((f, UsedOnlyM2MFilter))
                else:
                    smart_filters.append(f)
            else:
                smart_filters.append(f)

        return smart_filters

    def has_add_permission(self, request):
        return not (
            is_polymorphic_parent(self.model)
            and self.hide_base_class_from_index
        )

    def has_change_permission(self, request, obj=None):
        return not (
            is_polymorphic_parent(self.model)
            and self.hide_base_class_from_index
        )

    def has_delete_permission(self, request, obj=None):
        return not (
            is_polymorphic_parent(self.model)
            and self.hide_base_class_from_index
        )

    def get_model_perms(self, request):
        if (
            is_polymorphic_parent(self.model)
            and self.hide_base_class_from_index
        ) or self.hide_from_index:
            return {}  # Hide from admin index
        return super().get_model_perms(request)

    def __init__(self, model, admin_site):
        super().__init__(model=model, admin_site=admin_site)
        self.list_filter = self.smart_wrap_filters(self._get_list_filter())

        if not self.search_fields:
            self.search_fields = [
                f.name
                for f in model._meta.get_fields()
                if f.concrete
                and not f.many_to_many
                and not f.is_relation
                and isinstance(
                    f,
                    (
                        models.CharField,
                        models.DateField,
                        models.IntegerField,
                        models.TextField,
                    ),
                )
            ]

        self.formfield_overrides = {
            models.TextField: {
                "widget": Textarea(attrs={"spellcheck": "false"})
            },
        }

        app_label = model._meta.app_label
        model_name = model.__name__

        # try to fetch the generated form from the app's model_forms
        try:
            # dynamically import the app's forms module
            forms_module = import_module(f"{app_label}.forms")
            # fetch the form from model_forms dict
            self.form = getattr(forms_module, "model_forms", {}).get(
                f"{model_name}Form"
            )
        except ModuleNotFoundError:
            # fallback if forms.py doesn't exist
            self.form = None


def register_all_models(*, skip_models=None):
    """
    Auto-registers all models in the caller's app with BaseModelAdmin
    or with a custom admin class defined in the app's admin module.

    :param skip_models: set of model classes to skip (e.g., {MyModel})
    """
    skip_models = set(skip_models or [])

    app_config = get_calling_app_config()
    if not app_config:
        raise RuntimeError("Could not determine calling app")

    caller_module = sys.modules.get(f"{app_config.name}.admin")
    if caller_module is None:
        raise RuntimeError(f"Admin module not found for app {app_config.name}")

    for model in app_config.get_models():
        if model in skip_models:
            continue

        try:
            admin.site.unregister(model)
        except admin.sites.NotRegistered:
            pass

        admin_name = f"{model.__name__}Admin"
        if hasattr(caller_module, admin_name):
            admin_class = getattr(caller_module, admin_name)
        else:
            admin_class = BaseModelAdmin

        admin.site.register(model, admin_class)
