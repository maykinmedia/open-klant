from django.conf import settings

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
        {"name": "interne taken"},
        {"name": "klanten contacten"},
        {"name": "onderwerpobjecten"},
        {"name": "partij-identificatoren"},
        {"name": "partijen"},
        {"name": "rekeningnummers"},
        {"name": "vertegenwoordigingen"},
    ],
}
