from django.urls import path
from . import views
from .views import autocomplete_urls

app_name = 'kronika'

# fields autocomplete
urlpatterns = [] + autocomplete_urls