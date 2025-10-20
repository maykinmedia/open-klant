from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from solo.models import SingletonModel
from zgw_consumers.models import Service

from openklant.components.klantinteracties.models import Klantcontact
from referentielijsten_client.client import ReferentielijstenClient


class ReferentielijstenConfig(SingletonModel):
    enabled = models.BooleanField(
        default=False,
        help_text=_("Geef aan of Referentielijsten is ingeschakeld"),
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        help_text=_("De service waarmee referentielijstgegevens worden opgehaald"),
    )
    tabel_code = models.CharField(
        max_length=100,
        help_text=_("Code van de tabel die de kanaalopties bevat"),
    )

    def clean(self):
        if not self.enabled:
            return

        if not self.service or not self.tabel_code:
            raise ValidationError(
                "Service en tabel_code moeten zijn ingesteld wanneer validatie is ingeschakeld"
            )

        client = ReferentielijstenClient(service=self.service)
        items = client.get_items_by_tabel_code(self.tabel_code)
        valid_kanalen = {item.get("code") for item in items if item.get("code")}

        invalid = Klantcontact.objects.exclude(kanaal__in=valid_kanalen)
        if invalid.exists():
            raise ValidationError(
                f"Sommige bestaande Klantcontact.kanaal waarden zijn niet aanwezig "
                f"in Referentielijsten: {', '.join(invalid.values_list('kanaal', flat=True)[:5])}"
            )

    def __str__(self):
        return "Referentielijsten configuration"

    class Meta:
        verbose_name = "Referentielijsten configuration"
