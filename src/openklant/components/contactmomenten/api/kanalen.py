from django.conf import settings

from vng_api_common.notifications.kanalen import Kanaal

from openklant.components.contactmomenten.datamodel.models import ContactMoment

KANAAL_CONTACTMOMENTEN = Kanaal(
    settings.CONTACTMOMENTEN_NOTIFICATIONS_KANAAL,
    main_resource=ContactMoment,
    kenmerken=("bronorganisatie", "kanaal"),
)
