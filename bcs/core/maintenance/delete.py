from django.apps import apps
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models import ForeignKey, OneToOneField, ManyToManyField


def find_referencing_objects(obj):
    refs = []
    obj_model = obj.__class__
    obj_ct = ContentType.objects.get_for_model(obj)

    for model in apps.get_models():
        meta = model._meta

        # FK + OneToOne
        for field in meta.fields:
            if isinstance(field, (ForeignKey, OneToOneField)) and field.related_model == obj_model:
                qs = model.objects.filter(**{field.name: obj})
                refs.extend(qs)

        # ManyToMany
        for field in meta.many_to_many:
            if field.related_model == obj_model:
                qs = model.objects.filter(**{field.name: obj})
                refs.extend(qs)

        # GenericForeignKey
        for attr_name in dir(model):
            attr = getattr(model, attr_name)
            if isinstance(attr, GenericForeignKey):
                qs = model.objects.filter(
                    **{
                        attr.ct_field: obj_ct,
                        attr.fk_field: obj.pk,
                    }
                )
                refs.extend(qs)

    return refs
