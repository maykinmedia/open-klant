from django.conf import settings

# TODO: write a propper description
description = """
Description WIP.
"""

custom_settings = {
    "TITLE": "contactgegevens",
    "DESCRIPTION": description,
    "VERSION": settings.CONTACTGEGEVENS_API_VERSION,
    "SERVERS": [{"url": "/contactgegevens/api/v1"}],
    "TAGS": [
        {"name": "organisaties"},
        {"name": "personen"},
    ],
}
