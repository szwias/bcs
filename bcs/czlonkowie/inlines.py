from django.contrib.contenttypes.admin import GenericTabularInline
from .models import Osoby
from .forms import OsobyForm


class OsobyInline(GenericTabularInline):
    model = Osoby
    extra = 0
    form = OsobyForm