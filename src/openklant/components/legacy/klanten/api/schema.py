from django.conf import settings

from notifications_api_common.utils import notification_documentation

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

**API specificatie afwijkingen**

Afwijkingen in de API specificatie ten opzichte van de referentie API specificatie
zijn aangemerkt met ***AFWIJKING:**

**Autorisatie**

Deze API vereist autorisatie. Je kan de
[token-tool](https://zaken-auth.vng.cloud/) gebruiken om JWT-tokens te
genereren.

**Notificaties**

{notification_documentation(KANAAL_KLANTEN)}

**Handige links**

* [Documentatie](https://zaakgerichtwerken.vng.cloud/standaard)
* [Zaakgericht werken](https://zaakgerichtwerken.vng.cloud)
"""


custom_settings = {
    "TITLE": "Klanten API",
    "DESCRIPTION": description,
    "VERSION": settings.KLANTEN_API_VERSION,
    "APPEND_COMPONENTS": {
        "securitySchemes": {
            "JWT-Claims": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            }
        },
    },
}
