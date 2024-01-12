from django.conf import settings

# from drf_yasg import openapi
from notifications_api_common.utils import notification_documentation

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

info = {
    "TITLE": "Contactmomenten API",
    "DESCRIPTION": description,
    "VERSION": settings.CONTACTMOMENTEN_API_VERSION,
}
