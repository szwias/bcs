from django.contrib.postgres.search import SearchVector
from django.db.models import Value
from django.db.models.signals import post_save
from django.dispatch import receiver

from wyszukiwarka.models import AbstractSearchableModel


@receiver(post_save)
def update_search_vectors(sender, instance, **kwargs):
    if not issubclass(sender, (AbstractSearchableModel,)):
        return  # skip other models

    search_dict = instance._create_search_dict()
    flat_text = instance._flatten_search_dict()

    sender.objects.filter(pk=instance.pk).update(
        search_dict=search_dict,
        simple_tsv=SearchVector(Value(flat_text), config="simple"),
        tsv=SearchVector(Value(flat_text), config=instance.LANGUAGE),
    )
