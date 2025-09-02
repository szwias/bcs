from .views import autocomplete_urls

app_name = "miejsca_autocomplete"

urlpatterns = autocomplete_urls

from django.apps import apps

# Get the app config for the 'miejsca' app
app_config = apps.get_app_config("miejsca")
print(app_config)

# Get all models from that app
models = app_config.get_models()

# Example: print model names
for model in models:
    print(model.__name__)
