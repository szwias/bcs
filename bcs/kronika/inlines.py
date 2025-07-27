from django.contrib import admin

from .models import PodsumowanieKadencji
from .forms import PodsumowanieKadencjiForm


class PodsumowanieKadencjiInline(admin.StackedInline):
    model = PodsumowanieKadencji
    form = PodsumowanieKadencjiForm
    extra = 0
    fields = ["autor", "podsumowanie"]
    show_change_link = True
    ordering = ["autor"]
