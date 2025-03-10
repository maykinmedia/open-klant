from django.conf import settings
from django.utils.translation import gettext_lazy as _

description = _(
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

custom_settings = {
    "TITLE": "contactgegevens",
    "DESCRIPTION": description,
    "VERSION": settings.CONTACTGEGEVENS_API_VERSION,
    "SERVERS": [{"url": "/contactgegevens/api/v1"}],
    "TAGS": [
        {"name": "organisaties"},
        {"name": "personen"},
    ],
}
