from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from maykin_common.accounts.admin import PreventPrivilegeEscalationMixin

from .models import User


@admin.register(User)
class _UserAdmin(PreventPrivilegeEscalationMixin, UserAdmin):
    pass
