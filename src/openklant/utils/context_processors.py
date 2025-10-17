from django.conf import settings as django_settings


def settings(request):
    public_settings = (
        "GOOGLE_ANALYTICS_ID",
        "ENVIRONMENT",
        "SITE_TITLE",
        "PROJECT_NAME",
        "VNG_COMPONENTS_BRANCH",
        "ENVIRONMENT_SHOWN_IN_ADMIN",
    )

    context = {
        "settings": dict(
            [(k, getattr(django_settings, k, None)) for k in public_settings]
        ),
    }

    if hasattr(django_settings, "SENTRY_CONFIG"):
        context.update(dsn=django_settings.SENTRY_CONFIG.get("public_dsn", ""))

    return context
