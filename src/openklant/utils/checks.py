from collections.abc import Sequence

from django.apps import AppConfig, apps
from django.contrib import admin
from django.contrib.admin.options import BaseModelAdmin
from django.contrib.admin.utils import flatten as _flatten
from django.core.checks import CheckMessage, Error, register
from django.db import models

ALLOWED_UNOPTIMIZED_RELATIONS = {
    "config.ReferentielijstenConfig.service",
}


def _get_declared_field_names(model_admin: BaseModelAdmin) -> set[str] | None:
    if model_admin.fields:
        return set(_flatten(model_admin.fields))
    if model_admin.fieldsets:
        names: list[str] = []
        for _label, options in model_admin.fieldsets:
            names.extend(_flatten(options.get("fields", ())))
        return set(names)
    return None


def _resolve_inline_fk_name(
    inline_model: type[models.Model],
    parent_model: type[models.Model],
    fk_name: str | None,
) -> str | None:
    if fk_name:
        return fk_name

    candidates = [
        field.name
        for field in inline_model._meta.get_fields()
        if isinstance(field, models.ForeignKey) and field.related_model == parent_model
    ]
    if len(candidates) == 1:
        return candidates[0]
    return None


def _check_model_admin(
    model: type[models.Model],
    model_admin: BaseModelAdmin,
    fk_name: str | None = None,
) -> list[CheckMessage]:
    errors: list[CheckMessage] = []

    optimized_fields = set(model_admin.raw_id_fields) | set(
        model_admin.autocomplete_fields
    )
    excluded_fields = set(model_admin.exclude or ()) | set(
        model_admin.readonly_fields or ()
    )
    declared_fields = _get_declared_field_names(model_admin)

    for field in model._meta.get_fields():
        if not isinstance(field, models.ForeignKey):
            continue
        if isinstance(field, models.OneToOneField):
            continue
        if field.name == fk_name:
            continue
        if field.name in optimized_fields:
            continue
        if field.name in excluded_fields:
            continue
        if declared_fields is not None and field.name not in declared_fields:
            continue

        obj_label = f"{model._meta.label}.{field.name}"
        if obj_label in ALLOWED_UNOPTIMIZED_RELATIONS:
            continue

        errors.append(
            Error(
                f"{model_admin.__class__.__name__}.{field.name} is not optimized "
                "with raw_id_fields or autocomplete_fields.",
                hint=(
                    "Without raw_id_fields/autocomplete_fields, Django renders "
                    "this relation as a <select> populated with every row of "
                    "the related table, which can time out once that table "
                    "grows large. Add the field to raw_id_fields or "
                    "autocomplete_fields, or add it to ALLOWED_UNOPTIMIZED_RELATIONS "
                    "in openklant/utils/checks.py if the related table is "
                    "guaranteed to stay small."
                ),
                obj=obj_label,
                id="openklant.E001",
            )
        )

    for inline_class in getattr(model_admin, "inlines", ()):
        inline = inline_class(model_admin.model, admin.site)
        inline_fk_name = _resolve_inline_fk_name(
            inline.model, model_admin.model, inline.fk_name
        )
        errors.extend(_check_model_admin(inline.model, inline, fk_name=inline_fk_name))

    return errors


@register()
def check_admin_relation_fields(
    app_configs: Sequence[AppConfig] | None, **kwargs
) -> list[CheckMessage]:
    if app_configs is None:
        app_config_set = {
            ac
            for ac in apps.get_app_configs()
            if ac.name == "openklant" or ac.name.startswith("openklant.")
        }
    else:
        app_config_set = set(app_configs)

    errors: list[CheckMessage] = []
    for model, model_admin in admin.site._registry.items():
        if model._meta.app_config not in app_config_set:
            continue
        errors.extend(_check_model_admin(model, model_admin))
    return errors
