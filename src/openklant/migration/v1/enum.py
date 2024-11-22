from django.db.models import TextChoices


class KlantType(TextChoices):
    natuurlijk_persoon = "natuurlijk_persoon"
    niet_natuurlijk_persoon = "niet_natuurlijk_persoon"
    vestiging = "vestiging"
