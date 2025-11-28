from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

import structlog
from requests.exceptions import RequestException
from solo.models import SingletonModel
from zgw_consumers.client import build_client
from zgw_consumers.models import Service

from openklant.components.klantinteracties.models import Klantcontact
from referentielijsten_client.client import ReferentielijstenClient

logger = structlog.get_logger(__name__)


class ReferentielijstenConfig(SingletonModel):
    enabled = models.BooleanField(
        default=False,
        help_text=_(
            "Indicates whether or not the optional Referentielijsten API integration is enabled"
        ),
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        help_text=_(
            "The service used to retrieve information from the Referentielijsten API"
        ),
    )
    kanalen_tabel_code = models.CharField(
        max_length=100,
        help_text=_(
            "Code of the `tabel` that contains the possible `kanalen` (channels)"
        ),
        blank=True,
    )

    def clean(self):
        if not self.enabled:
            return

        if not self.service or not self.kanalen_tabel_code:
            raise ValidationError(
                _(
                    "Service en tabel_code moeten zijn ingesteld wanneer validatie is ingeschakeld"
                )
            )

        client = build_client(self.service, client_factory=ReferentielijstenClient)
        try:
            items = client.get_items_by_tabel_code(self.kanalen_tabel_code)
        except RequestException:
            logger.error(
                "failed_to_fetch_kanalen_from_referentielijsten",
                exc_info=True,
            )
            raise ValidationError(
                _(
                    "Er is een fout opgetreden bij het ophalen van de kanalen uit de Referentielijsten API."
                )
            )

        valid_kanalen = {item.get("code") for item in items if item.get("code")}

        invalid = Klantcontact.objects.exclude(kanaal__in=valid_kanalen)
        if invalid.exists():
            invalid_kanalen = ", ".join(
                invalid.values_list("kanaal", flat=True).order_by("kanaal").distinct()
            )
            raise ValidationError(
                _(
                    "Sommige bestaande Klantcontact.kanaal waarden zijn niet aanwezig "
                    "in Referentielijsten: {invalid_kanalen}"
                ).format(invalid_kanalen=invalid_kanalen)
            )

    def __str__(self):
        return "Referentielijsten configuration"

    class Meta:
        verbose_name = _("Referentielijsten configuration")
