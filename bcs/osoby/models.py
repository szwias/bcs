from django.contrib.contenttypes.models import ContentType
from django.db import transaction, connection
from roman import fromRoman

from django.contrib.postgres.fields import ArrayField

from core.utils.Lengths import (
    MAX_LENGTH,
    MEDIUM_LENGTH,
    SHORT_LENGTH,
    NAME_LENGTH,
)
from core.utils import Czas
from core.utils.Choices import TextAlt, TextChoose, IntAlt
from core.utils.Czas import ROK_ZALOZENIA
from czapki.models import Czapka
from kronika.models import Kadencja
from wyszukiwarka.utils.Search import *
from wyszukiwarka.models import SearchableModel, SearchablePolymorphicModel


class Lengths:
    AKTYWNOSC = 1
    STATUS = 2


class HallOfFame(SearchableModel):

    osoba = models.ForeignKey(
        "osoby.Osoba",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Osoba",
        related_name="wzmianka_w_hall_of_fame",
    )

    nazwa_alternatywna = models.CharField(
        max_length=MEDIUM_LENGTH, blank=True, verbose_name="Nazwa alternatywna"
    )

    zaslugi = models.CharField(max_length=MAX_LENGTH, verbose_name="Zasługi")

    # TODO: introduce a better ordering logic
    order_field = models.CharField(
        max_length=MAX_LENGTH, blank=True, editable=False
    )

    class Meta:
        verbose_name = "Hall of Fame"
        verbose_name_plural = "Hall of Fame"
        ordering = ["order_field"]

    def __str__(self):
        return f"{self.nazwa_alternatywna or self.osoba}: {self.zaslugi}"

    def save(self, *args, **kwargs):
        if not self.order_field:
            self.order_field = self.nazwa_alternatywna or str(self.osoba)
        super().save(*args, **kwargs)


class Byt(SearchablePolymorphicModel):
    pass


class KomisjaRewizyjna(Byt):
    search_indexable = True

    kadencja = models.ForeignKey(
        "kronika.Kadencja",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Kadencja",
    )

    przewodniczacy = models.ForeignKey(
        "osoby.Osoba",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Przewodniczący",
        related_name="przewodzi_komisjom",
    )

    sklad = models.ManyToManyField(
        "osoby.Osoba", blank=True, verbose_name="Skład"
    )

    dzialalnosc = models.TextField(
        blank=True, null=True, verbose_name="Działalność"
    )

    class Meta:
        verbose_name = "Komisja rewizyjna"
        verbose_name_plural = "Komisja rewizyjna"
        ordering = ["-kadencja"]

    def __str__(self):
        return f"Komisja rewizyjna {self.kadencja}"


# ORGANIZACJA FAMILY
# --------------------------------------
class Organizacja(Byt):
    search_indexable = True

    nazwa = models.CharField(
        max_length=MAX_LENGTH, verbose_name="Nazwa organizacji"
    )

    kraj = models.ForeignKey(
        "miejsca.Kraj",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Kraj",
    )

    siedziba = models.ForeignKey(
        "miejsca.Miejsce",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Siedziba",
    )

    zalozyciele = models.ManyToManyField(
        Byt,
        blank=True,
        verbose_name="Założyciele",
        related_name="zalozone_organizacje",
    )

    rok_zalozenia = models.IntegerField(
        choices=Czas.LATA_BRACTW + [IntAlt.DONT_KNOW],
        default=IntAlt.DONT_KNOW[0],
        verbose_name="Rok założenia",
    )

    opis = models.TextField(blank=True, verbose_name="Opis działalności")

    class Meta:
        verbose_name = "Organizacja"
        verbose_name_plural = "Organizacje"
        ordering = ["nazwa"]

    def __str__(self):
        return self.nazwa


class OrganizacjaStudencka(Organizacja):
    uczelnia = models.ForeignKey(
        "miejsca.Uczelnia",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Uczelnia",
    )

    class Meta:
        verbose_name = "Organizacja studencka"
        verbose_name_plural = "Organizacje studenckie"
        ordering = ["nazwa"]


class Bractwo(OrganizacjaStudencka):
    grupa_bractw = models.ForeignKey(
        "encyklopedia.GrupaBractw",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Grupa Bractw",
    )

    class Meta:
        verbose_name = "Bractwo"
        verbose_name_plural = "Bractwa"
        ordering = ["nazwa"]


# OSOBA FAMILY
# ---------------------------------------
class Osoba(Byt):
    imie = models.CharField(max_length=NAME_LENGTH, verbose_name="Imię")

    nazwisko = models.CharField(
        max_length=NAME_LENGTH, blank=True, verbose_name="Nazwisko"
    )

    przezwiska = ArrayField(
        models.CharField(max_length=MAX_LENGTH),
        blank=True,
        default=list,
        verbose_name="Przezwiska",
    )

    class Meta:
        verbose_name = "Osoba"
        verbose_name_plural = "Osoby"
        ordering = ("imie", "przezwiska", "nazwisko")

    def __str__(self):
        name = f"{self.imie}"
        if len(self.przezwiska) > 0:
            name += f' "{self.przezwiska[0]}'
            if len(self.przezwiska) > 1:
                name += f" / {self.przezwiska[1]}"
            name += '"'
        name += f" {self.nazwisko}"
        return name


class InnaOsoba(Osoba):
    search_indexable = True

    class Kategorie(models.TextChoices):
        INNA = "I", "Inna"
        INNE_BRACTWO_CZAPKOWE = "Inne BCS", "Inne bractwo czapkowe"
        ORGANIZACJA = "Org", "Organizacja"
        PRZYJACIEL_CZAPKI = "PC", "Przyjaciel Bractwa"

    opis = models.TextField(blank=True, verbose_name="Opis")

    kategoria = models.CharField(
        max_length=SHORT_LENGTH,
        default=Kategorie.INNA,
        choices=Kategorie.choices,
        verbose_name="Kategoria",
    )

    bractwo_do_ktorego_nalezy = models.ForeignKey(
        Bractwo,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Bractwo",
        related_name="czlonkowie_bractwa",
    )

    class Meta:
        verbose_name = "Inna osoba"
        verbose_name_plural = "Inne osoby (nie-członkowie)"
        ordering = ["imie", "nazwisko"]


class OsobaBCS(models.Model):
    class PewnoscStazu(models.TextChoices):
        TAK = "T", "Na pewno wcześniej się nie pojawiał"
        NIE = "N", "Ale mógł pojawić się wcześniej"

    czapka_1 = models.ForeignKey(
        "czapki.Czapka",
        on_delete=models.SET_NULL,
        null=True,
        default=Czapka.get_dont_know_czapka,
        verbose_name="Czapka",
        related_name="%(class)s_posiadacze_pierwszy_wybor",
    )

    czapka_2 = models.ForeignKey(
        "czapki.Czapka",
        on_delete=models.SET_NULL,
        null=True,
        default=Czapka.get_not_applicable_czapka,
        verbose_name="Inna czapka",
        related_name="%(class)s_posiadacze_drugi_wybor",
    )

    pierwsze_wydarzenie = models.ForeignKey(
        "kalendarz.Wydarzenie",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Pierwsze wydarzenie",
        related_name="%(class)s_nowi_beani",
    )

    staz = models.IntegerField(
        choices=Czas.LATA_BCS + [IntAlt.DONT_KNOW],
        default=2024,  # TODO: bieżący rok
        verbose_name="Rok pojawienia się",
    )

    pewnosc_stazu = models.CharField(
        choices=PewnoscStazu.choices,
        default=PewnoscStazu.TAK,
        verbose_name="Pewność roku pojawienia się",
    )

    class Meta:
        abstract = True


class Bean(Osoba, OsobaBCS):
    search_indexable = True

    rodzic_1 = models.ForeignKey(
        "osoby.Czlonek",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Rodzic czapkowy",
        related_name="beani_pierwszy_wybor",
    )

    rodzic_2 = models.ForeignKey(
        "osoby.Czlonek",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Drugi rodzic czapkowy",
        related_name="beani_drugi_wybor",
    )

    def baptize(self):
        with transaction.atomic():
            osoba_id = self.pk

            with connection.cursor() as cursor:
                cursor.execute(
                    f"DELETE FROM {Bean._meta.db_table} WHERE osoba_ptr_id = %s",
                    [osoba_id],
                )

            czlonek = Czlonek.objects.create(
                osoba_ptr_id=self.pk,
                imie=self.imie,
                nazwisko=self.nazwisko,
                przezwiska=self.przezwiska,
                staz=self.staz,
                status=Czlonek.Status.CZLONEK[0],
                pewnosc_stazu=self.pewnosc_stazu,
                czapka_1=self.czapka_1,
                czapka_2=self.czapka_2,
                aktywnosc=Czlonek.Aktywnosc.AKTYWNY[0],
                ochrzczony=TextChoose.YES[0],
                rodzic_1=self.rodzic_1,
                rodzic_2=self.rodzic_2,
            )

            return czlonek

    class Meta:
        verbose_name = "Bean"
        verbose_name_plural = "Beani"
        ordering = ["imie", "nazwisko"]


class Czlonek(Osoba, OsobaBCS):
    class Aktywnosc(models.TextChoices):
        AKTYWNY = (
            "A",
            "Aktywny",
        )
        AKTYWNY_MEDIALNIE = (
            "M",
            "Aktywny tylko w mediach",
        )
        NIEAKTYWNY = (
            "N",
            "Nieaktywny",
        )
        ODSZEDL = (
            "O",
            "Odszedł z grupy",
        )

    class Status(models.TextChoices):
        CZLONEK = "C", "Członek"
        WYKLETY = "X", 'Wydalony (np. "Jezus")'
        WETERAN = "W", "Weteran"
        HONOROWY = "H", "Członek Honoris Causa"

    search_indexable = True

    aktywnosc = models.CharField(
        max_length=Lengths.AKTYWNOSC,
        choices=Aktywnosc.choices,
        default=Aktywnosc.NIEAKTYWNY,
        verbose_name="Aktywność",
    )

    ochrzczony = models.CharField(
        max_length=max(TextAlt.LENGTH, TextChoose.LENGTH),
        choices=[*TextChoose.choices(), TextAlt.DONT_KNOW],
        default=TextAlt.DONT_KNOW[0],
        verbose_name="Czy ochrzczony",
    )

    chrzest = models.ForeignKey(
        "kalendarz.Chrzest",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Chrzest",
    )

    # TODO: add kalendarz.Wydarzenie records past 2023 so that you can fill
    #  column above and then remove following three fields

    rok_chrztu = models.IntegerField(
        choices=Czas.LATA_BCS + [IntAlt.DONT_KNOW] + [IntAlt.NOT_APPLICABLE],
        default=IntAlt.DONT_KNOW[0],
        verbose_name="Rok chrztu",
    )

    miesiac_chrztu = models.IntegerField(
        choices=Czas.MIESIACE + [IntAlt.DONT_KNOW] + [IntAlt.NOT_APPLICABLE],
        default=IntAlt.DONT_KNOW[0],
        verbose_name="Miesiąc chrztu",
    )

    dzien_chrztu = models.IntegerField(
        choices=Czas.DNI + [IntAlt.DONT_KNOW] + [IntAlt.NOT_APPLICABLE],
        default=IntAlt.DONT_KNOW[0],
        verbose_name="Dzień chrztu",
    )

    status = models.CharField(
        max_length=max(Lengths.STATUS, TextAlt.LENGTH),
        choices=Status.choices + [TextAlt.DONT_KNOW],
        default=TextAlt.DONT_KNOW[0],
        verbose_name="Status",
    )

    imie_piwne_1_wybor = models.CharField(
        max_length=TextAlt.LENGTH,
        choices=TextAlt.choices(),
        default=TextAlt.DONT_KNOW[0],
        verbose_name="Czy posiada imię czapkowe",
    )

    imie_piwne_1 = models.CharField(
        blank=True,
        max_length=MEDIUM_LENGTH,
        default="Nie wiem",
        verbose_name="Imię czapkowe",
    )

    imie_piwne_2_wybor = models.CharField(
        max_length=TextAlt.LENGTH,
        choices=TextAlt.choices(),
        default=TextAlt.NOT_APPLICABLE[0],
        verbose_name="Czy posiada inne imię czapkowe",
    )

    imie_piwne_2 = models.CharField(
        blank=True,
        max_length=MEDIUM_LENGTH,
        default="Nie dotyczy",
        verbose_name="Inne imię czapkowe",
    )

    rodzic_1 = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Rodzic czapkowy",
        related_name="dzieci_pierwszy_wybor",
    )

    rodzic_2 = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Drugi rodzic czapkowy",
        related_name="dzieci_drugi_wybor",
    )

    class Meta:
        verbose_name = "Członek"
        verbose_name_plural = "Członkowie"
        ordering = ["imie", "imie_piwne_1", "imie_piwne_2", "nazwisko"]

    def __str__(self):
        name = f"{self.imie} "
        nicknames = []

        if self.imie_piwne_1_wybor == "other":
            nicknames.append(self.imie_piwne_1)
            if self.imie_piwne_2_wybor == "other":
                nicknames.append(self.imie_piwne_2)
            elif self.przezwiska and self.przezwiska[0]:
                nicknames.append(self.przezwiska[0])
        elif self.przezwiska and self.przezwiska[0]:
            nicknames.append(self.przezwiska[0])
            if len(self.przezwiska) > 1 and self.przezwiska[1]:
                nicknames.append(self.przezwiska[1])

        if nicknames:
            name += f"\"{' / '.join(nicknames)}\" "

        name += self.nazwisko
        return name

    @staticmethod
    def get_dont_know_czlonek():
        czlonek = Czlonek.objects.get(
            imie="Nie",
            nazwisko="wiem",
            czapka_1=Czapka.get_dont_know_czapka(),
            czapka_2=Czapka.get_not_applicable_czapka(),
            staz=IntAlt.DONT_KNOW[0],
            pewnosc_stazu=OsobaBCS.PewnoscStazu.NIE,
            aktywnosc=Czlonek.Aktywnosc.NIEAKTYWNY,
            ochrzczony=TextChoose.YES[0],
            status=TextAlt.DONT_KNOW[0],
            rok_chrztu=ROK_ZALOZENIA,
            miesiac_chrztu=IntAlt.DONT_KNOW[0],
            dzien_chrztu=IntAlt.DONT_KNOW[0],
            imie_piwne_1_wybor=TextAlt.DONT_KNOW[0],
            imie_piwne_1="Nie wiem",
            imie_piwne_2_wybor=TextAlt.NOT_APPLICABLE[0],
            imie_piwne_2="Nie dotyczy",
        )
        return czlonek

    @staticmethod
    def get_not_applicable_czlonek():
        czlonek = Czlonek.objects.get(
            imie="Nie",
            nazwisko="dotyczy",
            czapka_1=Czapka.get_dont_know_czapka(),
            czapka_2=Czapka.get_not_applicable_czapka(),
            staz=IntAlt.DONT_KNOW[0],
            pewnosc_stazu=OsobaBCS.PewnoscStazu.TAK,
            aktywnosc=Czlonek.Aktywnosc.NIEAKTYWNY,
            ochrzczony=TextChoose.NO[0],
            status=TextAlt.DONT_KNOW[0],
            rok_chrztu=IntAlt.NOT_APPLICABLE[0],
            miesiac_chrztu=IntAlt.NOT_APPLICABLE[0],
            dzien_chrztu=IntAlt.NOT_APPLICABLE[0],
            imie_piwne_1_wybor=TextAlt.NOT_APPLICABLE[0],
            imie_piwne_1="Nie dotyczy",
            imie_piwne_2_wybor=TextAlt.NOT_APPLICABLE[0],
            imie_piwne_2="Nie dotyczy",
        )
        return czlonek

    def get_parents(self):
        return [p for p in [self.rodzic_1, self.rodzic_2] if p.exists()]

    def get_children(self):
        return list(self.dzieci_pierwszy_wybor.all())

    def get_step_children(self):
        return list(self.dzieci_drugi_wybor.all())

    def is_unknown(self):
        return self.imie == "Nie" and self.nazwisko == "wiem"

    def exists(self):
        return not (self.imie == "Nie" and self.nazwisko == "dotyczy")


# --------------------------------------- END


class ImieSzlacheckie(SearchableModel):
    imie = models.ForeignKey(
        Czlonek,
        on_delete=models.CASCADE,
        null=True,
        verbose_name="Imię szlacheckie",
    )

    class Meta:
        verbose_name = "Imię szlacheckie"
        verbose_name_plural = "Imiona szlacheckie"
        ordering = ["imie__imie_piwne_1", "imie__imie", "imie__nazwisko"]

    @property
    def posiadacz(self):
        return self.imie

    def __str__(self):
        name = f'"{self.imie.imie_piwne_1}" - {self.imie.imie}'
        if self.imie.nazwisko:
            name += f" {self.imie.nazwisko}"
        return name


# OSOBA DEPENDENT
# ------------------------------------------------------
class WielkiMistrz(SearchableModel):
    imie = models.ForeignKey(
        Czlonek,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Imię",
    )

    tadeusz = models.CharField(
        max_length=SHORT_LENGTH,
        verbose_name="Tadeusz",
    )

    tadeusz_numeric = models.IntegerField(
        editable=False, db_index=True, default=0
    )

    tytuly = models.TextField(blank=True, verbose_name="Tytuły")

    class Meta:
        verbose_name = "Wielki Mistrz"
        verbose_name_plural = "Wielcy Mistrzowie"
        ordering = ["-tadeusz_numeric"]

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


class Zespol(SearchableModel):
    nazwa = models.CharField(
        max_length=MEDIUM_LENGTH,
        verbose_name="Nazwa",
    )

    cel = models.TextField(
        blank=True,
        verbose_name="Cele",
    )

    czlonkowie = models.ManyToManyField(
        Osoba, blank=True, verbose_name="Członkowie"
    )

    dokument = models.ForeignKey(
        "zrodla.Dokument",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Dokument powołujący",
    )

    class Meta:
        verbose_name = "Zespół"
        verbose_name_plural = "Zespoły"
        ordering = ["-dokument__data", "nazwa"]

    @property
    def get_data(self):
        return "Data nieznana" if not self.dokument else self.dokument.data

    def __str__(self):
        return self.nazwa


class PrzewoZespolu(SearchableModel):
    osoba = models.ForeignKey(
        Osoba,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Osoba",
    )

    zespol = models.ForeignKey(
        Zespol,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Zespół",
    )

    rozpoczecie_urzedu = models.DateField(
        blank=True,
        null=True,
        verbose_name="Rozpoczęcie urzędu",
    )

    koniec_urzedu = models.DateField(
        blank=True,
        null=True,
        verbose_name="Koniec urzędu",
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f"{str(self.osoba)} - {str(self.zespol)}"


class KoordynatorZespolu(PrzewoZespolu):

    class Meta:
        verbose_name = "Koordynator Zespołu"
        verbose_name_plural = "Koordynatorzy zespołów"
        ordering = ["zespol", "-rozpoczecie_urzedu"]


class Egzekutor(PrzewoZespolu):

    class Meta:
        verbose_name = "Egzekutor"
        verbose_name_plural = "Egzekutorzy"
        ordering = ["zespol", "-rozpoczecie_urzedu"]


class ZwierzeCzapkowe(SearchableModel):
    czlonek = models.ForeignKey(
        Czlonek, on_delete=models.SET_NULL, null=True, verbose_name="Członek"
    )

    zwierze = models.CharField(
        max_length=MEDIUM_LENGTH, verbose_name="Zwierzę"
    )

    wyjasnienie = models.CharField(
        max_length=MEDIUM_LENGTH,
        blank=True,
        verbose_name="Wyjaśnienie (opcjonalne)",
    )

    class Meta:
        verbose_name = "Zwierzę czapkowe"
        verbose_name_plural = "Zwierzęta czapkowe"
        ordering = ["zwierze", "czlonek__imie_piwne_1"]

    @property
    def imie(self):
        return self.czlonek

    def __str__(self):
        name = f'"{self.czlonek.imie_piwne_1}" - {self.zwierze}'
        if self.wyjasnienie:
            name += f" ({self.wyjasnienie})"
        return name


# ZARZAD FAMILY
# ---------------------------------------
class Zarzad(Byt):
    kadencja = models.ForeignKey(
        Kadencja,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Kadencja",
    )

    wielki_mistrz = models.ForeignKey(
        "WielkiMistrz",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Wielki Mistrz",
        related_name="kadencje_jako_wielki_mistrz",
    )

    kasztelan = models.ForeignKey(
        Czlonek,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Kasztelan",
        related_name="kadencje_jako_kasztelan",
    )

    skarbnik = models.ForeignKey(
        Czlonek,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Skarbnik",
        related_name="kadencje_jako_skarbnik",
    )

    cantandi = models.ForeignKey(
        Czlonek,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Cantandi",
        related_name="kadencje_jako_cantandi_dawnego_zarzadu",
    )

    wybory = models.ForeignKey(
        "kronika.WydarzenieHistoryczne",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Wybory",
        related_name="zarzad_wybrany_na_wydarzeniu",
    )

    koniec_urzedu = models.ForeignKey(
        "kronika.WydarzenieHistoryczne",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Wydarzenie kończące urząd w tym składzie",
    )

    class Meta:
        verbose_name = "Zarząd"
        verbose_name_plural = "Zarządy"
        ordering = ["-wybory__wydarzenie__data_rozpoczecia"]

    def __str__(self):
        data_rozp = str(self.wybory.get_data) if self.wybory else "początek"
        data_zak = (
            str(self.koniec_urzedu.get_data)
            if self.koniec_urzedu
            else "koniec"
        )
        wm = str(self.wielki_mistrz.imie)
        return (
            f"Zarząd {str(self.kadencja)} - WM {wm}: {data_rozp} - {data_zak}"
        )


class DawnyZarzad(Zarzad):
    search_indexable = True

    bibendi = models.ForeignKey(
        Czlonek,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Bibendi",
        related_name="kadencje_jako_bibendi_dawnego_zarzadu",
    )

    magister_disciplinae = models.ForeignKey(
        Czlonek,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Magister Disciplinae",
        related_name="kadencje_jako_magister_disciplinae_dawnego_zarzadu",
    )

    kontakt_z_SSUJ = models.ForeignKey(
        Czlonek,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Kontakt Z SSUJ",
        related_name="kadencje_jako_kontakt_z_SSUJ_dawnego_zarzadu",
    )

    kontakt_z_SKNHI = models.ForeignKey(
        Czlonek,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Kontakt Z SKNHI",
        related_name="kadencje_jako_kontakt_z_SKNHI_dawnego_zarzadu",
    )

    class Meta:
        verbose_name = "Zarząd"
        verbose_name_plural = "Zarządy w starej formule"
        ordering = ["-kadencja"]


class NowyZarzad(Zarzad):
    search_indexable = True

    sekretarz = models.ForeignKey(
        Czlonek,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Sekretarz",
        related_name="kadencje_jako_sekretarz",
    )

    class Meta:
        verbose_name = "Zarząd"
        verbose_name_plural = "Zarządy w obecnej formule"
        ordering = ["-kadencja"]


# --------------------------------------- END

# TODO: add ZakonBractwowy model
