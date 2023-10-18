from django.conf import settings

from notifications_api_common.kanalen import Kanaal

from openklant.components.legacy.contactmomenten.models.contactmomenten import (
    ContactMoment,
)

KANAAL_CONTACTMOMENTEN = Kanaal(
    settings.CONTACTMOMENTEN_NOTIFICATIONS_KANAAL,
    main_resource=ContactMoment,
    kenmerken=("bronorganisatie", "kanaal"),
)
