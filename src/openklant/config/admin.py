from django.contrib import admin

from solo.admin import SingletonModelAdmin

from openklant.config.models import ReferentielijstenConfig


@admin.register(ReferentielijstenConfig)
class ReferentielijstenConfigAdmin(SingletonModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "enabled",
                    "service",
                    "kanalen_tabel_code",
                ),
            },
        ),
    )
