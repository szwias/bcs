from django.http import JsonResponse
from dal import autocomplete


class ChoiceAutocompleteByLabelMixin:
    def get_autocomplete_results(self, choices, *args, **kwargs):
        query = self.q.lower() if self.q else ""

        return [
            {"id": value, "text": label}
            for value, label in choices
            if query in label.lower()
        ]

    def get(self, request, *args, **kwargs):
        results = self.get_autocomplete_results(self.get_choices())
        return JsonResponse({"results": results})


class ChoiceAutocompleteByValueMixin:
    def get_autocomplete_results(self, choices, *args, **kwargs):
        query = self.q.lower() if self.q else ""
        return [
            {"id": value, "text": label}
            for value, label in choices
            if query in str(value).lower()
        ]

    def get(self, request, *args, **kwargs):
        results = self.get_autocomplete_results(self.get_choices())
        return JsonResponse({"results": results})


class FieldChoicesAutocompleteByLabel(
    ChoiceAutocompleteByLabelMixin, autocomplete.Select2ListView
):
    model = None
    field_name = None

    def get_choices(self):
        model_field = self.model._meta.get_field(self.field_name)
        return model_field.choices


class FieldChoicesAutocompleteByValue(
    ChoiceAutocompleteByValueMixin, autocomplete.Select2ListView
):
    model = None
    field_name = None

    def get_choices(self):
        model_field = self.model._meta.get_field(self.field_name)
        return model_field.choices


class StrMatchingAutocomplete(autocomplete.Select2QuerySetView):
    model = None

    def get_queryset(self):
        qs = self.model.objects.all()
        if self.q:
            qs = [obj for obj in qs if self.q.lower() in str(obj).lower()]
        return qs
