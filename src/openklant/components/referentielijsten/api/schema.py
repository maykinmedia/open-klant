from django.conf import settings

description = """
Een API om de referentielijsten in het domein klantinteracties te raadplegen en beheren.
""".strip()

# Spectacular settings overrides
custom_settings = {
    "TITLE": "Klantinteracties Referentielijsten",
    "VERSION": settings.REFERENTIELIJSTEN_API_VERSION,
    "DESCRIPTION": description,
    "SCHEMA_PATH_PREFIX_TRIM": True,
}
