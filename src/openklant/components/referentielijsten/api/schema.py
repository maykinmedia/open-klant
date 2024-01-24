from django.conf import settings

from drf_yasg import openapi

description = """
Een API om de referentielijsten in het domein klantinteracties te raadplegen en beheren.
""".strip()

info = openapi.Info(
    title="Klantinteracties Referentielijsten",
    default_version=settings.REFERENTIELIJSTEN_API_VERSION,
    description=description,
    contact=openapi.Contact(
        email="standaarden.ondersteuning@vng.nl",
        url="https://vng-realisatie.github.io/klantinteracties/",
    ),
    license=openapi.License(
        name="EUPL 1.2", url="https://opensource.org/licenses/EUPL-1.2"
    ),
)
