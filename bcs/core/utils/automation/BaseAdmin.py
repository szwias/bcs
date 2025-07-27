from django.contrib import admin
from django.contrib.admin.filters import RelatedFieldListFilter
from django.db.models import ForeignKey, ManyToManyField
from django.utils.module_loading import import_string
import inspect
from django.apps import apps
from django.db import models


class UsedOnlyFKFilter(RelatedFieldListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        # Determine which FK values are actually used
        used_ids = model.objects.values_list(field.name, flat=True).distinct()

        # Limit the field's queryset before calling the parent init
        self._original_limit_choices_to = field.remote_field.limit_choices_to
        field.remote_field.limit_choices_to = {"pk__in": used_ids}

        super().__init__(
            field, request, params, model, model_admin, field_path
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


class UsedOnlyM2MFilter(RelatedFieldListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        used_ids = get_used_m2m_ids(model, field.name)
        # Limit the choices shown in the filter dropdown
        self._original_limit_choices_to = field.remote_field.limit_choices_to
        field.remote_field.limit_choices_to = {"pk__in": used_ids}

        super().__init__(
            field, request, params, model, model_admin, field_path
        )

        # Restore original
        field.remote_field.limit_choices_to = self._original_limit_choices_to


class BaseModelAdmin(admin.ModelAdmin):

    actions = ["save_selected"]
    list_filter_exclude = set()
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

                if isinstance(field, ForeignKey):
                    smart_filters.append((f, UsedOnlyFKFilter))
                elif isinstance(field, ManyToManyField):
                    smart_filters.append((f, UsedOnlyM2MFilter))
                else:
                    smart_filters.append(f)
            else:
                smart_filters.append(f)

        return smart_filters

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)

        self.list_filter = self.smart_wrap_filters(self._get_list_filter())

        if not self.search_fields:
            self.search_fields = [
                f.name for f in model._meta.get_fields()
                if f.concrete and not f.many_to_many and not f.is_relation
                   and isinstance(f, (models.CharField, models.TextField))
            ]

        app_label = model._meta.app_label
        model_name = model.__name__
        form_path = f"{app_label}.forms.{model_name}Form"

        try:
            self.form = import_string(form_path)
        except ImportError:
            pass


def register_all_models(
    *, skip_models=None, custom_admins=None, base_admin_class=BaseModelAdmin
):
    """
    Auto-registers all models in the caller's app with BaseModelAdmin,
    unless overridden in `custom_admins`.

    :param skip_models: set of model classes to skip (e.g., {MyModel})
    :param custom_admins: dict mapping model classes to custom admin classes
    :param base_admin_class: default admin class to use if no custom one is provided
    """
    skip_models = set(skip_models or [])
    custom_admins = custom_admins or {}

    # Automatically infer the caller's app label
    caller_frame = inspect.stack()[1]
    caller_module = inspect.getmodule(caller_frame.frame)
    app_label = caller_module.__name__.split(".")[0]
    app_config = apps.get_app_config(app_label)

    for model in app_config.get_models():
        if model in skip_models:
            continue

        try:
            admin.site.unregister(model)
        except admin.sites.NotRegistered:
            pass

        admin_class = custom_admins.get(
            model, type(f"{model.__name__}Admin", (base_admin_class,), {})
        )

        admin.site.register(model, admin_class)
