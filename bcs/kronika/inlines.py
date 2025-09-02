from django.contrib import admin

from .models import PodsumowanieKadencji
from .forms import model_forms


class PodsumowanieKadencjiInline(admin.StackedInline):
    model = PodsumowanieKadencji
    form = model_forms["PodsumowanieKadencjiForm"]
    extra = 0
    fields = ["autor", "podsumowanie"]
    show_change_link = True
    ordering = ["autor"]
