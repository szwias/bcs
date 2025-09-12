from polymorphic.models import PolymorphicModel


def is_base_polymorphic_model(model):
    """
    Returns True if `model` is a base polymorphic class
    (i.e., the top-most class in its inheritance chain).
    """
    return model == model._meta.get_base_class() and issubclass(
        model, PolymorphicModel
    )


def is_leaf_polymorphic_model(model):
    """
    Returns True if `model` is a leaf in its polymorphic hierarchy
    (no other model inherits from it).
    """
    # Only polymorphic models
    if not issubclass(model, PolymorphicModel):
        return False

    # Check if any other model subclass this one
    for subclass in PolymorphicModel.__subclasses__():
        if issubclass(subclass, model) and subclass != model:
            return False
    return True


from django.db.models import Func, TextField, Value


class JsonExtractText(Func):
    function = "jsonb_extract_path_text"
    output_field = TextField()

    def __init__(self, expression, key, **extra):
        super().__init__(expression, Value(key), **extra)
