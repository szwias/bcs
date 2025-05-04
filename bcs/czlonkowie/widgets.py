from dal import autocomplete

class TabSafeModelSelect2(autocomplete.ModelSelect2):
    class Media:
        js = ['czlonkowie/js/tabindex-fix.js']

class TabSafeListSelect2(autocomplete.ListSelect2):
    class Media:
        js = ['czlonkowie/js/tabindex-fix.js']
