from django.contrib.admin.options import InlineModelAdmin


class ParentAwareInline(InlineModelAdmin):
    """
    Base Inline admin that injects the parent object into each inline form via `parent_obj` kwarg.
    """

    def get_formset(self, request, obj=None, **kwargs):
        formset_class = self.get_parent_aware_formset_class(obj)
        kwargs["formset"] = formset_class
        return super().get_formset(request, obj, **kwargs)

    def get_parent_aware_formset_class(self, parent_obj):
        BaseFormSet = self.formset  # typically BaseInlineFormSet

        class ParentAwareFormSet(BaseFormSet):
            def get_form_kwargs(self, index):
                form_kwargs = super().get_form_kwargs(index)
                form_kwargs["parent_obj"] = parent_obj
                return form_kwargs

        return ParentAwareFormSet
