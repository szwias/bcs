from django.db import models
from roman import fromRoman
from core.utils import Consts
from core.utils.Consts import MAX_LENGTH, MEDIUM_LENGTH, SHORT_LENGTH
from core.utils.czas import Czas
from core.utils.czas.models import Kadencja


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


class Lengths:
    UCZELNIE = 10
    AKTYWNOSC = 1
    STATUS = 2
    WYDZIAL = 10

class Czapka(models.Model):
    class Uczelnie(models.TextChoices):
        UJ = "UJ", "UJ"
        AGH = "AGH", "AGH"
        PK = "PK", "PK"
        UEK = "UEK", "UEK"
        UW = "UW", "UW"
        SLASKI = "UŚ", "UŚ"
        LODZKI = "UŁ", "UŁ"
        UP_L = "UP_L", "Uniwersytet Przyrodniczy w Lublinie"
        NIEMCY = "NIEMCY", "Niemcy"
        DONT_KNOW = "XXX", "Nie wiem"
        NOT_APPLICABLE = "n/a", "Nie dotyczy"
    WydzialChoices = {
        Uczelnie.UJ: [
            ("WPiA", "Wydział Prawa i Administracji"),
            ("CMUJ", "Collegium Medicum"),
            ("WFarm", "Wydział Farmaceutyczny"),
            ("WNoZ", "Wydział Nauk o Zdrowiu"),
            ("WFiloz", "Wydział Filozoficzny"),
            ("WHist", "Wydział Historyczny"),
            ("WFilol", "Wydział Filologiczny"),
            ("WPol", "Wydział Polonistyki"),
            ("WFAiIS", "Wydział Fizyki, Astronomii i Informatyki Stosowanej"),
            ("WMiI", "Wydział Matematyki i Informatyki"),
            ("WChUJ", "Wydział Chemii"),
            ("WB", "Wydział Biologii"),
            ("WZiKS", "Wydział Zarządzania i Komunikacji Społecznej"),
            ("WSMiP", "Wydział Studiów Międzynarodowych i Politycznych"),
            ("WBBiB", "Wydział Biochemii, Biofizyki i Biotechnologii"),
            ("WGiG", "Wydział Geografii i Geologii"),
            ("SMP", "Studia Matematyczno-Przyrodnicze"),
            ("Honorowa", "Honoris Causa")
        ],
        Uczelnie.AGH: [
            ("PG", "Pion górniczy"),
            ("PH", "Pion hutniczy"),
            ("Inne", "Inne"),
        ],
        Uczelnie.PK: [
            ("WA", "Wydział Architektury"),
            ("WM", "Wydział Mechaniczny"),
            ("WIL", "Wydział Inżynierii Lądowej")
        ],
        Uczelnie.UEK: [
            ("UEK", "Dowolny wydział"),
        ],
        Uczelnie.UW: [
            ("UW", "Dowolny wydział"),
        ],
        Uczelnie.SLASKI: [
            ("US", "Dowolny wydział"),
        ],
        Uczelnie.LODZKI: [
            ("UL", "Dowolny wydział"),
        ],
        Uczelnie.UP_L: [
            ("UP_L", "Dowolny wydział"),
        ],
        Uczelnie.DONT_KNOW: [
            ("XXX", "Nie wiem"),
        ],
        Uczelnie.NOT_APPLICABLE: [
            ("n/a", "Nie dotyczy"),
        ],
        Uczelnie.NIEMCY: [
            ("XXX", "Nie wiem"),
        ]
    }

    uczelnia = models.CharField(
        max_length=Lengths.UCZELNIE,
        choices = Uczelnie.choices,
        default=Uczelnie.UJ,
        verbose_name='Uczelnia',
    )

    wydzial = models.CharField(
        max_length=Lengths.WYDZIAL,
        default=("XXX", "Nie wiem"),
        verbose_name='Wydział',
    )

    kolor = models.CharField(
        max_length=Consts.MAX_LENGTH,
        default='',
        verbose_name='Kolor',
    )

    class Meta:
        verbose_name = "Czapka"
        verbose_name_plural = "Czapki"
        ordering = ['uczelnia', 'kolor', 'wydzial']

    def __str__(self):
        if self.uczelnia == self.Uczelnie.NOT_APPLICABLE:
            return "Nie dotyczy"
        if self.uczelnia == self.Uczelnie.DONT_KNOW:
            return "Nie wiem"
        return str(self.uczelnia) + "_" + str(self.kolor) + "_" + str(self.wydzial)

    @staticmethod
    def get_dont_know_czapka():
        return Czapka.objects.get_or_create(uczelnia=Czapka.Uczelnie.DONT_KNOW)

    @staticmethod
    def get_not_applicable_czapka():
        return Czapka.objects.get_or_create(uczelnia=Czapka.Uczelnie.NOT_APPLICABLE)

class Czlonek(models.Model):
    class Aktywnosc(models.TextChoices):
        AKTYWNY = 'A', "Aktywny",
        AKTYWNY_MEDIALNIE = 'M', "Aktywny tylko w mediach",
        NIEAKTYWNY = 'N', "Nieaktywny",
        ODSZEDL = 'O', "Odszedł z grupy",
    class Status(models.TextChoices):
        BEAN = "B", "Bean"
        CZLONEK = "C", "Członek"
        WYKLETY = "X", "Wydalony (np. \"Jezus\")"
        WETERAN = "W", "Weteran"
        HONOROWY = "H", "Członek Honoris Causa"
        # BEAN_PRIM = "BP", "Bean lub Członek"
        # CZLONEK_PRIM = "CP", "Członek lub Weteran"

    imie = models.CharField(
        max_length=40,
        verbose_name='Imię'
    )

    nazwisko = models.CharField(
        max_length=40,
        blank=True,
        verbose_name='Nazwisko'
    )

    aktywnosc = models.CharField(
        max_length=Lengths.AKTYWNOSC,
        choices=Aktywnosc.choices,
        default=Aktywnosc.NIEAKTYWNY,
        verbose_name='Aktywność'
    )

    czapka_1 = models.ForeignKey(
        Czapka,
        on_delete=models.SET_NULL,
        null=True,
        default=Czapka.get_dont_know_czapka,
        verbose_name="Czapka",
        related_name="czapka_1"
    )

    czapka_2 = models.ForeignKey(
        Czapka,
        on_delete=models.SET_NULL,
        null=True,
        default=Czapka.get_not_applicable_czapka,
        verbose_name="Inna czapka",
        related_name="czapka_2"
    )

    ochrzczony = models.CharField(
        max_length=max(TextAlt.LENGTH, TextChoose.LENGTH),
        choices=[
            *TextChoose.choices(),
            TextAlt.DONT_KNOW
        ],
        default=TextAlt.DONT_KNOW,
        verbose_name="Ochrzczony?",
    )

    rok_chrztu = models.IntegerField(
        choices=Czas.LATA + [IntAlt.DONT_KNOW] + [IntAlt.NOT_APPLICABLE],
        default=IntAlt.DONT_KNOW,
        verbose_name='Rok chrztu'
    )

    miesiac_chrztu = models.IntegerField(
        choices=Czas.MIESIACE + [IntAlt.DONT_KNOW] + [IntAlt.NOT_APPLICABLE],
        default=IntAlt.DONT_KNOW,
        verbose_name='Miesiąc chrztu'
    )

    dzien_chrztu = models.IntegerField(
        choices=Czas.DNI + [IntAlt.DONT_KNOW] + [IntAlt.NOT_APPLICABLE],
        default=IntAlt.DONT_KNOW,
        verbose_name='Dzień chrztu'
    )

    staz = models.IntegerField(
        choices=Czas.LATA + [IntAlt.DONT_KNOW],
        default=IntAlt.DONT_KNOW,
        verbose_name='Rok pojawienia się'
    )

    pewnosc_stazu = models.BooleanField(
        choices=[
            (True, "Na pewno wcześniej się nie pojawiał"),
            (False, "Ale mógł pojawić się wcześniej")
        ],
        default=(False, "Ale mógł pojawić się wcześniej"),
        verbose_name="Pewność daty stażu"
    )

    status = models.CharField(
        max_length=max(Lengths.STATUS, TextAlt.LENGTH),
        choices=Status.choices + [TextAlt.DONT_KNOW],
        default=TextAlt.DONT_KNOW,
        verbose_name='Status'
    )

    imie_piwne_1_wybor = models.CharField(
        max_length=TextAlt.LENGTH,
        choices=[
            TextAlt.DONT_KNOW,
            TextAlt.NOT_APPLICABLE,
            ("other", "Posiada"),
        ],
        default=TextAlt.DONT_KNOW,
        verbose_name="Imię czapkowe"
    )

    imie_piwne_1 = models.CharField(
        max_length=100,
        default="Nie wiem",
        verbose_name="Wpisz imię czapkowe:"
    )

    imie_piwne_2_wybor = models.CharField(
        max_length=TextAlt.LENGTH,
        choices=[
            TextAlt.NOT_APPLICABLE,
            ("other", "Posiada"),
        ],
        default=TextAlt.NOT_APPLICABLE,
        verbose_name="Inne imię czapkowe"
    )

    imie_piwne_2 = models.CharField(
        max_length=100,
        default="Nie dotyczy",
        verbose_name="Wpisz inne imię czapkowe:"
    )

    rodzic_1 = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name="Rodzic czapkowy",
        related_name='rodzic_1_set',
    )

    rodzic_2 = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name="Drugi rodzic czapkowy",
        related_name='rodzic_2_set',
    )

    class Meta:
        verbose_name = "Członek"
        verbose_name_plural = "Członkowie"
        ordering = ['imie', 'imie_piwne_1', 'imie_piwne_2', 'nazwisko']

    def __str__(self):
        name = str(self.imie) + " "
        if self.imie_piwne_1_wybor == "other":
            name += "\"" + str(self.imie_piwne_1)
            if self.imie_piwne_2_wybor == "other":
                name += "/" + str(self.imie_piwne_2)
            name += "\" "
        name += str(self.nazwisko)
        return name

class Przezwisko(models.Model):
    kto = models.ForeignKey(
        Czlonek,
        on_delete=models.CASCADE,
        verbose_name="Kto"
    )

    przezwisko = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name="Przezwisko"
    )

    class Meta:
        verbose_name = "Przezwisko"
        verbose_name_plural = "Przezwiska"
        ordering = ['kto', 'przezwisko']

    def __str__(self):
        return f"{self.kto} - {self.przezwisko}"

class ImieSzlacheckie(models.Model):
    imie = models.ForeignKey(
        Czlonek,
        on_delete=models.CASCADE,
        null=True,
        verbose_name="Imię szlacheckie",
    )

    class Meta:
        verbose_name = "Imię szlacheckie"
        verbose_name_plural = "Imiona szlacheckie"
        ordering = ['imie__imie_piwne_1', 'imie__imie', 'imie__nazwisko']

    @property
    def posiadacz(self):
        return self.imie

    def __str__(self):
        name = f"\"{self.imie.imie_piwne_1}\" - {self.imie.imie}"
        if self.imie.nazwisko:
            name += f" {self.imie.nazwisko}"
        return name

class ZwierzeCzapkowe(models.Model):
    czlonek = models.ForeignKey(
        Czlonek,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Członek"
    )

    zwierze = models.CharField(
        max_length=100,
        verbose_name="Zwierzę"
    )

    wyjasnienie = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Wyjaśnienie (opcjonalne)"
    )

    class Meta:
        verbose_name = "Zwierzę czapkowe"
        verbose_name_plural = "Zwierzęta czapkowe"
        ordering = ['zwierze', 'czlonek__imie_piwne_1']

    @property
    def imie(self):
        return self.czlonek

    def __str__(self):
        name =  f"\"{self.czlonek.imie_piwne_1}\" - {self.zwierze}"
        if self.wyjasnienie:
            name += f" ({self.wyjasnienie})"
        return name

class DawnyZarzad(models.Model):
    kadencja = models.ForeignKey(
        Kadencja,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Kadencja",
    )

    wielki_mistrz = models.ForeignKey(
    Czlonek,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Wielki Mistrz",
        related_name="dz_wielki_mistrz",
    )

    kasztelan = models.ForeignKey(
        Czlonek,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Kasztelan",
        related_name="dz_kasztelan",
    )

    skarbnik = models.ForeignKey(
       Czlonek,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Skarbnik",
        related_name="dz_skarbnik",
    )

    bibendi = models.ForeignKey(
        Czlonek,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Bibendi",
        related_name="dz_bibendi",
    )

    magister_disciplinae = models.ForeignKey(
        Czlonek,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Magister Disciplinae",
        related_name="dz_magister_disciplinae",
    )

    cantandi = models.ForeignKey(
        Czlonek,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Cantandi",
        related_name="dz_cantandi",
    )

    kontakt_z_SSUJ = models.ForeignKey(
        Czlonek,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Kontakt Z SSUJ",
        related_name="dz_kontakt_z_SSUJ",
    )

    kontakt_z_SKNHI = models.ForeignKey(
        Czlonek,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Kontakt Z SKNHI",
        related_name="dz_kontakt_z_SKNHI",
    )

    class Meta:
        verbose_name = "Dawny Zarząd"
        verbose_name_plural = "Dawne Zarządy"
        ordering = ['-kadencja']

    def __str__(self):
        return f"Zarząd {str(self.kadencja)}"

class Zarzad(models.Model):
    kadencja = models.ForeignKey(
        Kadencja,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Kadencja",
    )

    wielki_mistrz = models.ForeignKey(
        Czlonek,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Wielki Mistrz",
        related_name="wielki_mistrz",
    )

    kasztelan = models.ForeignKey(
        Czlonek,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Kasztelan",
        related_name="kasztelan",
    )

    skarbnik = models.ForeignKey(
        Czlonek,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Skarbnik",
        related_name="skarbnik",
    )

    cantandi = models.ForeignKey(
        Czlonek,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Cantandi",
        related_name="cantandi",
    )

    sekretarz = models.ForeignKey(
        Czlonek,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Sekretarz",
        related_name="sekretarz",
    )

    class Meta:
        verbose_name = "Zarząd"
        verbose_name_plural = "Zarządy"
        ordering = ['-kadencja']

    def __str__(self):
        return f"Zarząd {str(self.kadencja)}"

class WielkiMistrz(models.Model):
    imie = models.ForeignKey(
        Czlonek,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Imię",
    )

    tadeusz = models.CharField(
        max_length=10,
        verbose_name="Tadeusz",
    )

    tadeusz_numeric = models.IntegerField(
        editable=False,
        db_index=True,
        default=0,
    )

    tytuly = models.TextField(
        blank=True,
        verbose_name="Tytuły",
    )

    class Meta:
        verbose_name = "Wielki Mistrz"
        verbose_name_plural = "Wielcy Mistrzowie"
        ordering = ['-tadeusz_numeric']

    def __str__(self):
        name = f"{str(self.imie)} - Tadeusz {self.tadeusz}"
        if self.tytuly:
            name += f", {self.tytuly}"
        return name

    def save(self, *args, **kwargs):
        try:
            self.tadeusz_numeric = fromRoman(str(self.tadeusz).upper())
        except ValueError:
            self.tadeusz_numeric = 0
        super().save(*args, **kwargs)

class HallOfFame(models.Model):
    czlonek = models.ForeignKey(
        Czlonek,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Członek",
    )

    nazwa_alternatywna = models.CharField(
        max_length=MEDIUM_LENGTH,
        blank=True,
        verbose_name="Nazwa alternatywna",
    )

    zaslugi = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name="Zasługi",
    )

    order_field = models.CharField(
        max_length=MAX_LENGTH,
        blank=True,
        editable=False,
    )

    class Meta:
        verbose_name = "Hall of Fame"
        verbose_name_plural = "Hall of Fame"
        ordering = ['order_field']


    def __str__(self):
        return str(self.nazwa_alternatywna or self.czlonek)

    def  save(self, *args, **kwargs):
        if not self.order_field:
            self.order_field = self.nazwa_alternatywna if self.nazwa_alternatywna else str(self.czlonek)
        super().save(*args, **kwargs)

class InnaOsoba(models.Model):
    class Kategorie(models.TextChoices):
        INNA = "I", "Inna"
        INNE_BRACTWO_CZAPKOWE = "Inne BCS", "Inne bractwo czapkowe"
        ORGANIZACJA = "Org", "Organizacja"
        PRZYJACIEL_CZAPKI = "PC", "Przyjaciel Bractwa"

    nazwa = models.CharField(
        max_length=MEDIUM_LENGTH,
        verbose_name="Nazwa",
    )

    opis = models.TextField(
        blank=True,
        verbose_name="Opis",
    )

    kategoria = models.CharField(
        max_length=SHORT_LENGTH,
        default=Kategorie.INNA,
        choices=Kategorie.choices,
        verbose_name="Kategoria",
    )

    class Meta:
        verbose_name = "Inna osoba"
        verbose_name_plural = "Inne osoby (nie-członkowie)"
        ordering = ['nazwa']

    def __str__(self):
        return f"{self.nazwa}"

