from django.contrib.admin import StackedInline
from .forms import model_forms
from .models import (
    PrawoObowiazek,
)


class PrawoObowiazekInline(StackedInline):
    model = PrawoObowiazek
    form = model_forms["PrawoObowiazekForm"]
    extra = 0
