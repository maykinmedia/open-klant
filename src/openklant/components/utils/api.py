def get_related_object_uuid(obj: object, attr: str) -> str | None:
    """
    Extract the UUID as a string from a related object.

    :param obj: The main object.
    :param attr: The name of related object.
    :return: UUID as a string, or None if not found.
    """
    related_obj = getattr(obj, attr, None)
    uuid = getattr(related_obj, "uuid", None)
    return str(uuid) if uuid else None
