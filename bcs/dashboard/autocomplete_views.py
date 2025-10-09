from dal import autocomplete

from core.autocompletion.registry import register_autocomplete
from dashboard.utils import list_named_urls

autocomplete_urls, autocomplete_widgets = register_autocomplete(overrides={})


class CustomAppDjangoUrlAutocomplete(autocomplete.Select2ListView):
    def get_list(self):
        """Return all URLs or filter by namespace passed via query params."""
        namespace = self.forwarded.get("aplikacja")  # from 'tytul' field
        urls = list_named_urls()
        if namespace:
            urls = [u for u in urls if u.startswith(namespace)]
        return urls
