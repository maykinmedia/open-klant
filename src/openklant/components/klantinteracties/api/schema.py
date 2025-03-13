from django.conf import settings

from notifications_api_common.utils import notification_documentation

from openklant.components.klantinteracties.kanalen import (
    KANAAL_INTERNETAAK,
    KANAAL_PARTIJ,
)

# TODO: write a propper description
description = """
Description WIP.
"""

custom_settings = {
    "TITLE": "klantinteracties",
    "DESCRIPTION": description,
    "VERSION": settings.KLANTINTERACTIES_API_VERSION,
    "SERVERS": [{"url": "/klantinteracties/api/v1"}],
    "TAGS": [
        {"name": "actoren"},
        {"name": "actor klantcontacten"},
        {"name": "betrokkenen"},
        {"name": "bijlagen"},
        {"name": "categorie relaties"},
        {"name": "categorieën"},
        {"name": "digitale adressen"},
        {
            "name": "interne taken",
            "description": f"{notification_documentation(KANAAL_INTERNETAAK)}",
        },
        {"name": "klanten contacten"},
        {"name": "onderwerpobjecten"},
        {"name": "partij-identificatoren"},
        {
            "name": "partijen",
            "description": f"{notification_documentation(KANAAL_PARTIJ)}",
        },
        {"name": "rekeningnummers"},
        {"name": "vertegenwoordigingen"},
    ],
}
