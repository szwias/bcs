from django.contrib import admin

from .forms import model_forms
from .models import PodsumowanieKadencji


class PodsumowanieKadencjiInline(admin.StackedInline):
    model = PodsumowanieKadencji
    form = model_forms["PodsumowanieKadencjiForm"]
    extra = 0
    fields = ["autor", "podsumowanie"]
    show_change_link = True
    ordering = ["autor"]
