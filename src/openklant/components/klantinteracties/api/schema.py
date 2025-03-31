from django.conf import settings
from django.utils.translation import gettext_lazy as _

from notifications_api_common.utils import notification_documentation

from openklant.components.klantinteracties.kanalen import (
    KANAAL_INTERNETAAK,
    KANAAL_PARTIJ,
)

DESCRIPTION = _(
    """
**Warning: Difference between `PUT` and `PATCH`**

Both `PUT` and `PATCH` methods can be used to update the fields in a resource,
but there is a key difference in how they handle required fields:

* The `PUT` method requires you to specify **all mandatory fields** when updating a resource.
If any mandatory field is missing, the update will fail. Optional fields are left unchanged if they are not specified.

* The `PATCH` method, on the other hand, allows you to update only the fields you specify.
Some mandatory fields can be left out, and the resource will only be updated with the provided data,
leaving other fields unchanged.
"""
)
PARTIJ_IDENTIFICATOR_DESCRIPTION_CREATE = _(
    """
**Warnings:**

Handles `partijIdentificatoren` creation with atomicity guarantees.

- If the `UUID` is provided in the `PartijIdentificator` object,
the endpoint will treat it as an update operation for the existing `PartijIdentificator`,
applying the provided data and linking the parent `Partij` to the updated `PartijIdentificator`.
- If the `UUID` is **NOT** specified, the system will create a new
`PartijIdentificator` instance respecting all uniqueness constraints.

**Example:**

```json
{
  "partijIdentificatoren": [
    {
      "uuid": "095be615-a8ad-4c33-8e9c-c7612fbf6c9f",
      "partijIdentificator": {
        "codeObjecttype": "niet_natuurlijk_persoon",
        "codeSoortObjectId": "rsin",
        "objectId": "string",
        "codeRegister": "hr"
      }
    },
    {
      "partijIdentificator": {
        "codeObjecttype": "natuurlijk_persoon",
        "codeSoortObjectId": "bsn",
        "objectId": "string",
        "codeRegister": "brp"
      }
    }
  ]
}
```


In this case, the `PartijIdentificator` with the specified `UUID` is updated and attached to the parent `Partij`,
 while the `PartijIdentificator` without a `UUID` is created and attached to the parent `Partij`.
"""
)

PARTIJ_IDENTIFICATOR_DESCRIPTION_UPDATE = _(
    """
**Warnings:**

Handles `partijIdentificatoren` updates with atomicity guarantees.

- If the `UUID` is specified in the `PartijIdentificator` object,
 the system will update the corresponding instance with the new data.
- If the `UUID` is **NOT** specified, the system will `DELETE` all `partijIdentificatoren`
objects related to the parent and `CREATE` new ones using the provided data.

**Example:**

```json
{
  "partijIdentificatoren": [
    {
      "uuid": "095be615-a8ad-4c33-8e9c-c7612fbf6c9f",
      "partijIdentificator": {
        "codeObjecttype": "niet_natuurlijk_persoon",
        "codeSoortObjectId": "rsin",
        "objectId": "string",
        "codeRegister": "hr"
      }
    },
    {
      "partijIdentificator": {
        "codeObjecttype": "natuurlijk_persoon",
        "codeSoortObjectId": "bsn",
        "objectId": "string",
        "codeRegister": "brp"
      }
    }
  ]
}
```

In this case, all `partijIdentificatoren` without a specified `UUID` are deleted,
a new one is created due to the absence of a `UUID`, and the data for the `PartijIdentificator`
with the specified `UUID` is then updated.
"""
)

PARTIJEN_DESCRIPTION = (
    _(
        """
**Atomicity in Partij and PartijIdentificator**

The `Partij` endpoint handles `PartijIdentificator` objects more effectively,
allowing them to be processed within the same request.
This ensures that both entities are handled atomically, preventing incompleteness,
and offering better control over the uniqueness of `PartijIdentificator` objects.

For `POST`, `PATCH`, and `PUT` requests for `Partij`,
it is possible to send a list of `PartijIdentificator` objects.


"""
    )
    + notification_documentation(KANAAL_PARTIJ)
)


custom_settings = {
    "TITLE": "klantinteracties",
    "DESCRIPTION": DESCRIPTION,
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
        {"name": "partijen", "description": PARTIJEN_DESCRIPTION},
        {"name": "rekeningnummers"},
        {"name": "vertegenwoordigingen"},
    ],
}
