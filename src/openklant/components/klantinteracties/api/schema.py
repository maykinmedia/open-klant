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

PARTIJEN_DESCRIPTION = _(
    """
**Atomicity in Partij and PartijIdentificator**

The `Partij` endpoint handles `partijIdentificator` objects more effectively,
allowing them to be processed within the same request.
This ensures that both entities are handled atomically, preventing incompleteness,
and offering better control over the uniqueness of `partijIdentificator` objects.

For `POST`, `PATCH`, and `PUT` requests for `Partij`,
it is possible to send a list of `partijIdentificator` objects.


"""
) + notification_documentation(KANAAL_PARTIJ)

PARTIJ_IDENTIFICATOREN_DESCRIPTION = _(
    """
### **Uniqueness of Partij and PartijIdentificator**

The following description defines the constraints applied to the `PartijIdentificator`
model to ensure data integrity, enforce both **global** and **local** uniqueness,
and support **hierarchical** relationships between identifiers.
These constraints also cover specific behaviors related to register
hierarchies and are essential for maintaining consistency within and across `Partij` entities.


Each `PartijIdentificator` is validated according to a predefined registry hierarchy.
The `object_id` is validated in the context of its `code_soort_object_id`,
and the registry (`code_register`) determines the expected structure.

The registry configuration is as follows:


| codeRegister  | codeObjecttype       | codeSoortObjectId                |
|---------------|--------------------------|------------------------------|
| brp           | natuurlijk_persoon       | bsn,                         |
| hr            | niet_natuurlijk_persoon  | rsin, kvk_nummer,            |
| hr            | vestiging                | vestigingsnummer,            |



**1. Global Uniqueness**

The `PartijIdentificator` must be globally unique.
This means that the following combination of fields must appear only once across all records:

- `codeObjecttype`
- `codeSoortObjectId`
- `objectId`
- `codeRegister`

This ensures that each `partijIdentificatoren` is distinct and not duplicated across the system.

**2. Local Uniqueness Within a Partij**

Within a single `Partij`, it is not allowed to have multiple `partijIdentificatoren` entries
with the same `codeSoortObjectId`.

For example: a single `Partij` cannot have two `partijIdentificatoren` of `bsn`.
Each `codeSoortObjectId` can only appear once per `Partij`.


**3. Introduction of `subIdentificatorVan` field**

To support hierarchical relationships between `partijIdentificatoren` entries such as the relationship between a
`vestigingsnummer` and its corresponding `kvk_nummer`, a new field called `subIdentificatorVan` has been introduced.

This field is a foreign key referencing another `PartijIdentificator`, establishing a parent-child structure
between identifiers.
By default, the `subIdentificatorVan` field is nullable for most of entries, except
for a `vestigingsnummer`, where it must be set to a valid `kvk_nummer`.
The referenced `kvk_nummer` can belong to the same `Partij`, to an external one, or it can be
created independently without being associated with any `Partij`.

In all cases, a `vestigingsnummer` cannot exist without being linked to a valid
`kvk_nummer` through the `subIdentificatorVan` field.


**Warnings:**


- The original global uniqueness constraints still applies with this additional field:

  - If `subIdentificatorVan` is `null`, then the combination of `PartijIdentificator` fields must be unique.
  - If `subIdentificatorVan` is set, then the combination `subIdentificatorVan`
  and `PartijIdentificator` fields must be unique.

- A `PartijIdentificator` cannot reference itself through the `subIdentificatorVan` field.
The reference must always point to a different `PartijIdentificator` to avoid self-referencing.

**4. Deletion or Modification Restrictions**

A `PartijIdentificator` that has other `partijIdentificatoren` entries linked to it
cannot be deleted or modified directly.

For example: If a `kvk_nummer` has one or more `vestigingsnummer` identifiers linked to it,
those `vestigingsnummer` entries must first be deleted or updated before the `kvk_nummer`
itself can be modified or removed.

"""
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
        {
            "name": "partij-identificatoren",
            "description": PARTIJ_IDENTIFICATOREN_DESCRIPTION,
        },
        {
            "name": "partijen",
            "description": PARTIJEN_DESCRIPTION,
        },
        {"name": "rekeningnummers"},
        {"name": "vertegenwoordigingen"},
    ],
}
