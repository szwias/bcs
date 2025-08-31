from django.contrib.admin import StackedInline
from .forms import PrawoObowiazekForm
from .models import (
    PrawoObowiazek,
)


class PrawoObowiazekInline(StackedInline):
    model = PrawoObowiazek
    form = PrawoObowiazekForm
    extra = 0
