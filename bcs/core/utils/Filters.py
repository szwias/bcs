from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.apps import apps


class UsedContentTypeFilter(admin.SimpleListFilter):
    """
    :param title: filter title
    :param parameter_name: for URL lookup
    """

    def lookups(self, request, model_admin):
        # Get only content types that are actually used in this model
        used_ct_ids = model_admin.model.objects.values_list(
            "polymorphic_ctype", flat=True
        ).distinct()
        used_cts = ContentType.objects.filter(id__in=used_ct_ids)
        return [
            (ct.id, apps.get_model(ct.app_label, ct.model)._meta.verbose_name)
            for ct in used_cts
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(polymorphic_ctype_id=self.value())
        return queryset
