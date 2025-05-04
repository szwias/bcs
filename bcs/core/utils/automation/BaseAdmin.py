from django.contrib import admin
from django.utils.module_loading import import_string
import inspect
from django.apps import apps

class BaseModelAdmin(admin.ModelAdmin):
    actions = ['save_selected']
    save_as = True

    def save_selected(self, request, queryset):
        for obj in queryset:
            obj.save()

        self.message_user(request, "Saved selected objects successfully")

    save_selected.short_description = "Saved selected objects"

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)

        app_label = model._meta.app_label
        model_name = model.__name__
        form_path = f"{app_label}.forms.{model_name}Form"

        try:
            self.form = import_string(form_path)
        except ImportError:
            pass


def register_all_models(*, skip_models=None, custom_admins=None):
    """
    Auto-registers all models in the caller's app with BaseModelAdmin,
    unless overridden in `custom_admins`.

    :param skip_models: set of model names to skip
    :param custom_admins: dict mapping model classes to custom admin classes
    """
    # Determine caller app label automatically
    caller_frame = inspect.stack()[1]
    caller_module = inspect.getmodule(caller_frame[0])
    app_label = caller_module.__name__.split('.')[0]

    skip_models = set(skip_models or [])
    custom_admins = custom_admins or {}

    app_config = apps.get_app_config(app_label)

    for model in app_config.get_models():
        if model.__name__ in skip_models:
            continue

        try:
            admin.site.unregister(model)
        except admin.sites.NotRegistered:
            pass

        admin_class = custom_admins.get(model, type(f'{model.__name__}Admin', (BaseModelAdmin,), {}))
        admin.site.register(model, admin_class)