from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

import structlog
from requests.exceptions import RequestException, Timeout
from rest_framework import status
from solo.models import SingletonModel
from zgw_consumers.models import Service

from openklant.components.klantinteracties.models import Klantcontact
from referentielijsten_client.client import (
    REFERENTIELIJST_CLIENT_CACHE_PREFIX,
    get_referentielijsten_client,
)

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

        try:
            with get_referentielijsten_client(self.service) as client:
                items = client.get_items_by_tabel_code(self.kanalen_tabel_code)
        except (RequestException, Exception):
            logger.exception("failed_to_fetch_kanalen_from_referentielijsten")
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

    def save(self, *args, **kwargs):
        if self.kanalen_tabel_code:
            cache.delete(
                f"{REFERENTIELIJST_CLIENT_CACHE_PREFIX}{self.kanalen_tabel_code}"
            )
        return super().save(*args, **kwargs)

    @property
    def connection_check(self):
        if not self.service or not self.kanalen_tabel_code:
            return _(
                "Not performing connection check, service and/or kanalen tabel code are not configured"
            ), None

        try:
            with get_referentielijsten_client(self.service) as client:
                if client.can_connect:
                    items = client.get_cached_items_by_tabel_code(
                        self.kanalen_tabel_code
                    )
                    return items, status.HTTP_200_OK
                return _("Unable to connect to Referentielijsten API"), None
        except Timeout:
            return _(
                "Request to Referentielijsten API timed out"
            ), status.HTTP_504_GATEWAY_TIMEOUT
        except RequestException:
            return _("Unable to retrieve items from Referentielijsten API"), None

    def __str__(self):
        return "Referentielijsten configuration"

    class Meta:
        verbose_name = _("Referentielijsten configuration")
