# # drzewo/drzewo.py
# from django import forms
# from osoby.models import Czlonek
# from core.utils.Choices import TextChoose
# from core.utils.Czas import MAKSYMALNA_ILOSC_POKOLEN
#
#
# class FullTreeRenderForm(forms.Form):
#     only_known_parents = forms.BooleanField(
#         required=False, label="Pokaż tylko członków o znanych rodzicach"
#     )
#
#
# class ScopedTreeRenderForm(forms.Form):
#     member = forms.ModelChoiceField(
#         queryset=Czlonek.objects.filter(ochrzczony=TextChoose.YES[0]).exclude(
#             id=Czlonek.get_dont_know_czlonek().id
#         ),
#         required=True,
#         label="Członek, dla którego chcesz wygenerować drzewo",
#     )
#     depth = forms.IntegerField(
#         min_value=0,
#         max_value=MAKSYMALNA_ILOSC_POKOLEN,
#         required=True,
#         label="Ilość pokoleń potomków",
#     )
#     gen = forms.IntegerField(
#         min_value=0,
#         max_value=MAKSYMALNA_ILOSC_POKOLEN,
#         required=False,
#         label="Ilość pokoleń wstecz - zostaw puste, by dotrzeć do korzenia drzewa",
#     )
#     only_known_parents = forms.BooleanField(
#         required=False, label="Pokaż tylko członków o znanych rodzicach"
#     )
#
#     def __init__(self, *args, **kwargs):  # TODO: add autocompletion
#         super().__init__(*args, **kwargs)
#         # self.fields['member'].widget = autocomplete.ModelSelect2(
#         #     url='osoby_autocomplete:czlonek-records-autocomplete'
#         # )
#
#     def clean_gen(self):
#         gen = self.cleaned_data.get("gen")
#         if gen is None:
#             return MAKSYMALNA_ILOSC_POKOLEN
#         return gen
