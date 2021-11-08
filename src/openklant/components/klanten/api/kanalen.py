from django.conf import settings

from vng_api_common.notifications.kanalen import Kanaal

from openklant.components.klanten.datamodel.models import Klant

KANAAL_KLANTEN = Kanaal(
    settings.KLANTEN_NOTIFICATIONS_KANAAL,
    main_resource=Klant,
    kenmerken=("subject_type",),
)
