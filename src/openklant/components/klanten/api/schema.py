from django.conf import settings

from drf_yasg import openapi
from vng_api_common.notifications.utils import notification_documentation

from .kanalen import KANAAL_KLANTEN

description = f"""Een API om klanten te benaderen.

Een API om zowel klanten te registreren als op te vragen. Een klant
is een natuurlijk persoon, niet-natuurlijk persoon (bedrijf) of vestiging
waarbij het gaat om niet geverifieerde gegevens. De Klanten API kan
zelfstandig of met andere API's samen werken om tot volledige functionaliteit
te komen.

**Afhankelijkheden**

Deze API is afhankelijk van:

* Autorisaties API
* Notificaties API
* Zaken API *(optioneel)*
* Documenten API *(optioneel)*

**Autorisatie**

Deze API vereist autorisatie. Je kan de
[token-tool](https://zaken-auth.vng.cloud/) gebruiken om JWT-tokens te
genereren.

** Notificaties

{notification_documentation(KANAAL_KLANTEN)}

**Handige links**

* [Documentatie](https://zaakgerichtwerken.vng.cloud/standaard)
* [Zaakgericht werken](https://zaakgerichtwerken.vng.cloud)
"""

info = openapi.Info(
    title="Klanten API",
    default_version=settings.KLANTEN_API_VERSION,
    description=description,
    contact=openapi.Contact(
        email="standaarden.ondersteuning@vng.nl",
        url="https://zaakgerichtwerken.vng.cloud",
    ),
    license=openapi.License(
        name="EUPL 1.2", url="https://opensource.org/licenses/EUPL-1.2"
    ),
)
