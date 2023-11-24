from django.conf import settings

from drf_yasg import openapi

# TODO: write a propper description
description = """
Description WIP.
"""

info = openapi.Info(
    title="klantinteracties",
    default_version=settings.KLANTINTERACTIES_API_VERSION,
    description=description,
    contact=openapi.Contact(
        email="standaarden.ondersteuning@vng.nl",
        url="https://zaakgerichtwerken.vng.cloud",
    ),
    license=openapi.License(
        name="EUPL 1.2", url="https://opensource.org/licenses/EUPL-1.2"
    ),
)
