from django.contrib import admin

from osoby.forms import model_forms
from osoby.models import KoordynatorZespolu, Egzekutor, InnaOsoba


class KoordynatorZespoluInline(admin.StackedInline):
    model = KoordynatorZespolu
    form = model_forms["KoordynatorZespoluForm"]
    extra = 0
    fields = ["osoba", "rozpoczecie_urzedu", "koniec_urzedu"]
    show_change_link = True
    ordering = ["rozpoczecie_urzedu"]


class EgzekutorInline(KoordynatorZespoluInline):
    model = Egzekutor
    form = model_forms["EgzekutorForm"]


class InnaOsobaInline(admin.StackedInline):
    model = InnaOsoba
    form = model_forms["InnaOsobaForm"]
    extra = 0
    fields = ["imie", "nazwisko", "przezwiska"]
    show_change_link = True
    ordering = ["imie", "nazwisko", "przezwiska"]
