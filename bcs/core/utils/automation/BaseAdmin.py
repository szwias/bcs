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


def register_all_models(*, skip_models=None, custom_admins=None, base_admin_class=BaseModelAdmin):
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
    app_label = caller_module.__name__.split('.')[0]
    app_config = apps.get_app_config(app_label)

    for model in app_config.get_models():
        if model in skip_models:
            continue

        try:
            admin.site.unregister(model)
        except admin.sites.NotRegistered:
            pass

        admin_class = custom_admins.get(
            model,
            type(f'{model.__name__}Admin', (base_admin_class,), {})
        )

        admin.site.register(model, admin_class)