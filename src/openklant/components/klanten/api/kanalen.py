from django.conf import settings
from notifications_api_common.kanalen import Kanaal

from openklant.components.klanten.models.klanten import Klant

KANAAL_KLANTEN = Kanaal(
    settings.KLANTEN_NOTIFICATIONS_KANAAL,
    main_resource=Klant,
    kenmerken=("subject_type",),
)
