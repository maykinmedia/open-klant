from django.conf import settings

from drf_yasg import openapi
from vng_api_common.notifications.utils import notification_documentation

from .kanalen import KANAAL_CONTACTMOMENTEN

description = f"""Een API om contactmomenten met klanten te registreren of op
te vragen.

**Afhankelijkheden**

Deze API is afhankelijk van:

* Autorisaties API
* Notificaties API
* Klanten API
* Zaken API *(optioneel)*
* Verzoeken API *(optioneel)*
* Documenten API *(optioneel)*

**API specificatie afwijkingen**

Afwijkingen in de API specificatie ten opzichte van de referentie API specificatie
zijn aangemerkt met ***AFWIJKING:**

**Autorisatie**

Deze API vereist autorisatie. Je kan de
[token-tool](https://zaken-auth.vng.cloud/) gebruiken om JWT-tokens te
genereren.

**Notificaties**

{notification_documentation(KANAAL_CONTACTMOMENTEN)}

**Handige links**

* [Documentatie](https://zaakgerichtwerken.vng.cloud/standaard)
* [Zaakgericht werken](https://zaakgerichtwerken.vng.cloud)
"""

info = openapi.Info(
    title="Contactmomenten API",
    default_version=settings.CONTACTMOMENTEN_API_VERSION,
    description=description,
    contact=openapi.Contact(
        email="standaarden.ondersteuning@vng.nl",
        url="https://zaakgerichtwerken.vng.cloud",
    ),
    license=openapi.License(
        name="EUPL 1.2", url="https://opensource.org/licenses/EUPL-1.2"
    ),
)
