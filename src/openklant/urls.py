from django.apps import apps
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path, re_path
from django.views.generic.base import TemplateView

from openklant.accounts.views.password_reset import PasswordResetView

# from two_factor.admin import AdminSiteOTPRequired
# from two_factor.urls import urlpatterns as tf_urls


handler500 = "openklant.utils.views.server_error"
admin.site.site_header = "openklant admin"
admin.site.site_title = "openklant admin"
admin.site.index_title = "Welcome to the openklant admin"

# # This will cause users not to be able to login any longer without the OTP setup. There are some
# # issues in this package that need to be resolved.
# admin.site.__class__ = AdminSiteOTPRequired

urlpatterns = [
    path(
        "admin/password_reset/",
        PasswordResetView.as_view(),
        name="admin_password_reset",
    ),
    path(
        "admin/password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path("admin/", admin.site.urls),
    # path("admin/", include(tf_urls)),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path(
        "klantinteracties/api/",
        include("openklant.components.klantinteracties.api.urls"),
    ),
    path(
        "contactgegevens/api/",
        include("openklant.components.contactgegevens.api.urls"),
    ),
    # Simply show the master template.
    path("", TemplateView.as_view(template_name="main.html")),
    # separate apps
    re_path(
        r"^(?P<component>klantinteracties|contactgegevens)/$",
        TemplateView.as_view(template_name="index.html"),
        name="main",
    ),
    path("ref/", include("vng_api_common.urls")),
    path("oidc/", include("mozilla_django_oidc.urls")),
]

# NOTE: The staticfiles_urlpatterns also discovers static files (ie. no need to run collectstatic). Both the static
# folder and the media folder are only served via Django if DEBUG = True.
urlpatterns += staticfiles_urlpatterns() + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

if settings.DEBUG and apps.is_installed("debug_toolbar"):
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
