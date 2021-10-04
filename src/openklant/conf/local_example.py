#
# Any machine specific settings when using development settings.
#

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "openklant",
        "USER": "openklant",
        "PASSWORD": "openklant",
        "HOST": "",  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        "PORT": "",  # Set to empty string for default.
    }
}
