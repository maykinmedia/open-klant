from django.conf import settings
from django.utils.translation import gettext_lazy as _

from notifications_api_common.utils import notification_documentation

from openklant.components.klantinteracties.kanalen import (
    KANAAL_INTERNETAAK,
    KANAAL_PARTIJ,
)

# TODO: write a propper description
description = """
Description WIP.
description = _(
    """
**Warning: Difference between `PUT` and `PATCH`**

Both `PUT` and `PATCH` methods are used to update the fields in a resource,
but there is a key difference in how they handle required fields:

> The `PUT` method requires you to specify **all mandatory fields** when updating a resource.
If any mandatory field is missing, the update will fail.

> The `PATCH` method, on the other hand, allows you to update only the fields you specify.
Some mandatory fields can be left out, and the resource will only be updated with the provided data,
leaving other fields unchanged.
"""
)
partijen_description = _(
    """
**Atomicity in Partij and PartijIdentificator**

Starting from version **2.7.0**, the `Partij` endpoint has been modified to handle
`PartijIdentificator` objects more effectively,
allowing them to be processed within the same request.
This ensures that both entities are handled atomically, preventing incomplete,
and offering better control over the uniqueness of `PartijIdentificator` objects.

For `POST`, `PATCH`, and `PUT` requests for `Partij`,
it is possible to send a list of `PartijIdentificator` objects.

**Warnings:**

- In all requests, `PartijIdentificator` objects should not contain the **UUID**
of the parent `Partij`, because it is automatically assigned.
- `POST` request:
    - If the **UUID** is provided in the `PartijIdentificator` object,
    the endpoint will treat it as an update operation for the existing `PartijIdentificator`,
    applying the provided data and linking the parent `Partij` to the new one created.
    - If the **UUID** is **not** specified, the system will create a new resource
    for the `PartijIdentificator` respecting all uniqueness constraints.
- `PATCH` or `PUT` requests:
    - If the **UUID** is provided in the `PartijIdentificator` object,
    the system will update the specified resource with the new data.
    - If the **UUID** is **not** specified, the system will `DELETE` all `PartijIdentificator`
    objects related to the parent and `CREATE` new ones with the passed data.
"""
)

custom_settings = {
    "TITLE": "klantinteracties",
    "DESCRIPTION": description,
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
        {
            "name": "partijen",
            "description": f"{notification_documentation(KANAAL_PARTIJ)}",
        },
        {"name": "partijen", "description": partijen_description},
        {"name": "rekeningnummers"},
        {"name": "vertegenwoordigingen"},
    ],
}
