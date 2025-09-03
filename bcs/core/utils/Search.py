from textwrap import shorten
from core.utils.Lengths import SNIPPET_LENGTH
from core.models import SearchableModel


def snip(instance, text):
    title = instance._meta.verbose_name
    desc = shorten(text, width=SNIPPET_LENGTH, placeholder="...")
    return f"{title}: [{desc}]"
