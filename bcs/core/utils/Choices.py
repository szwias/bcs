class TextChoose:
    YES = "T", "Tak"
    NO = "N", "Nie"

    LENGTH = 1

    @classmethod
    def choices(cls):
        return [cls.YES, cls.NO]

class TextAlt:
    NOT_APPLICABLE = "n/a", "Nie dotyczy"
    DONT_KNOW = "d/n", "Nie wiem"
    NEGATIVE_CHOICES = [NOT_APPLICABLE, DONT_KNOW]
    OTHER = "other", "Other"

    LENGTH = 5

    @classmethod
    def choices(cls):
        return [cls.NOT_APPLICABLE, cls.DONT_KNOW, cls.OTHER]

class IntAlt:
    NOT_APPLICABLE = 1010101010, "Nie dotyczy"
    DONT_KNOW = 1111111111, "Nie wiem"
    NEGATIVE_CHOICES = [NOT_APPLICABLE, DONT_KNOW]
    OTHER = 2222222222, "Other"

    @classmethod
    def choices(cls):
        return [cls.NOT_APPLICABLE, cls.DONT_KNOW, cls.OTHER]