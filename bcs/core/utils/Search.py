from textwrap import shorten
from core.utils.Lengths import SNIPPET_LENGTH


def snip(text):
    return shorten(text, width=SNIPPET_LENGTH, placeholder="...")
