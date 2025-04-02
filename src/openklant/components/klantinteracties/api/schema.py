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

- If the `UUID` is provided in the `partijIdentificator` object,
the endpoint will treat it as an update operation for the existing `partijIdentificator`,
applying the provided data and linking the parent `Partij` to the updated `partijIdentificator`.
- If the `UUID` is **NOT** specified, the system will create a new
`partijIdentificator` instance respecting all uniqueness constraints.

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


In this case, the `partijIdentificator` with the specified `UUID` is updated and attached to the parent `Partij`,
 while the `partijIdentificator` without a `UUID` is created and attached to the parent `Partij`.

**Warnings:**

If you want to create a `partijIdentificator` with `vestigingsnummer`,
you must first ensure that a `partijIdentificator`
with a `kvk_nummer` already exists to assign it at the `sub_identificator_van`.

**Example:**

```json
{
  "partijIdentificatoren": [
      {
          "sub_identificator_van": {"uuid": "598ffc4d-737e-49a5-b5e0-cbc438a30cb5"},
          "partijIdentificator": {
              "codeObjecttype": "vestiging",
              "codeSoortObjectId": "vestigingsnummer",
              "objectId": "string",
              "codeRegister": "hr",
          },
      }
  ],
}
```

Or, to comply with the uniqueness constraints, you must first make a `POST` request
 to create the `partijIdentificator` with `kvk_nummer`,
and then send a `PUT` or `PATCH` request to update the list of `partijIdentificatoren`
 by adding the `partijIdentificator` with `vestigingsnummer`.
See the documentation for `PUT` and `PATCH` requests in the corresponding section.

"""
)

PARTIJ_IDENTIFICATOR_DESCRIPTION_UPDATE = _(
    """
**Warnings:**

Handles `partijIdentificatoren` updates with atomicity guarantees.

- If the `UUID` is specified in the `partijIdentificator` object,
 the system will update the corresponding instance with the new data.
- If the `UUID` is **NOT** specified, the system will `DELETE` all `partijIdentificatoren`
objects related to the parent and `CREATE` new ones using the provided data.
This means that any `partijIdentificatoren` **not included** in the list new data will also be deleted.

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

In this case, assuming an initial state with 3 `partijIdentificatoren` for the current `Partij`,
 the system will perform the following operations:
  - All initial `partijIdentificatoren` not included in the list, as well as those
  without a specified `UUID`, will be deleted.
  - `partijIdentificator` with `codeSoortObjectId` = `rsin`, will be updated with the new data provided
  - All other `partijIdentificatoren` without a specified `UUID` will be created.

"""
)

PARTIJEN_DESCRIPTION = (
    _(
        """
**Atomicity in Partij and PartijIdentificator**

The `Partij` endpoint handles `partijIdentificator` objects more effectively,
allowing them to be processed within the same request.
This ensures that both entities are handled atomically, preventing incompleteness,
and offering better control over the uniqueness of `partijIdentificator` objects.

For `POST`, `PATCH`, and `PUT` requests for `Partij`,
it is possible to send a list of `partijIdentificator` objects.


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
