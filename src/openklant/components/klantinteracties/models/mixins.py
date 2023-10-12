from django.db import models
from django.utils.translation import gettext_lazy as _

from vng_api_common.descriptors import GegevensGroepType


class ActorIdentifcatorMixin(models.Model):
    actoridentifcator_objecttype = models.CharField(
        _("Objecttype"),
        help_text=_(
            "Type van het object, bijvoorbeeld: 'INGESCHREVEN NATUURLIJK PERSOON'."
        ),
        max_length=200,
        blank=False,
    )
    actoridentifcator_soort_object_id = models.CharField(
        _("Soort Object ID"),
        help_text=_(
            "Naam van de eigenschap die het object identificeert, bijvoorbeeld: 'Burgerservicenummer'."
        ),
        max_length=200,
        blank=False,
    )
    actoridentifcator_object_id = models.CharField(
        _("Object ID"),
        help_text=_(
            "Waarde van de eigenschap die het object identificeert, bijvoorbeeld: '123456788'."
        ),
        max_length=200,
        blank=False,
    )
    actoridentifcator_register = models.CharField(
        _("Object ID"),
        help_text=_(
            "Binnen het landschap van registers unieke omschrijving van het register waarin "
            "het object is geregistreerd, bijvoorbeeld: 'BRP'."
        ),
        max_length=200,
        blank=False,
    )

    actoridentifcator = GegevensGroepType(
        {
            "objecttype": actoridentifcator_objecttype,
            "soort object id": actoridentifcator_soort_object_id,
            "object id": actoridentifcator_object_id,
            "register": actoridentifcator_register,
        }
    )

    class Meta:
        abstract = True
