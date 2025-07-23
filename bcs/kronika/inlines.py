from django.contrib import admin

from .models import CharakterystykaDzialanZarzadu
from .forms import CharakterystykaDzialanZarzaduForm


class CharakterystykaDzialanZarzaduInline(admin.StackedInline):
    model = CharakterystykaDzialanZarzadu
    form = CharakterystykaDzialanZarzaduForm
    extra = 0
    fields = ["autor", "charakterystyka"]
    show_change_link = True
    ordering = ["autor"]
