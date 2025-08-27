from django.contrib import admin

from osoby.forms import KoordynatorZespoluForm
from osoby.models import KoordynatorZespolu


class KoordynatorZespoluInline(admin.StackedInline):
    model = KoordynatorZespolu
    form = KoordynatorZespoluForm
    extra = 0
    fields = ["osoba", "rozpoczecie_urzedu", "koniec_urzedu"]
    show_change_link = True
    ordering = ["rozpoczecie_urzedu"]