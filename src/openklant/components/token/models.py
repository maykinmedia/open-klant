from django.db import models
from django.utils.translation import gettext_lazy as _

from openklant.components.token.utils import get_token
from openklant.components.token.validators import validate_non_empty_chars


class TokenAuth(models.Model):
    identifier = models.SlugField(
        unique=True, help_text=_("A human-friendly label to refer to this token")
    )

    token = models.CharField(
        _("token"),
        max_length=40,
        unique=True,
        validators=[validate_non_empty_chars]
    )

    contact_person = models.CharField(
        _("contact person"),
        max_length=200,
        help_text=_("Name of the person in the organization who can access the API"),
    )
    email = models.EmailField(
        _("email"), help_text=_("Email of the person, who can access the API")
    )
    organization = models.CharField(
        _("organization"),
        max_length=200,
        blank=True,
        help_text=_("Organization which has access to the API"),
    )
    last_modified = models.DateTimeField(
        _("last modified"),
        auto_now=True,
        help_text=_("Last date when the token was modified"),
    )
    created = models.DateTimeField(
        _("created"), auto_now_add=True, help_text=_("Date when the token was created")
    )
    application = models.CharField(
        _("application"),
        max_length=200,
        blank=True,
        help_text=_("Application which has access to the API"),
    )
    administration = models.CharField(
        _("administration"),
        max_length=200,
        blank=True,
        help_text=_("Administration which has access to the API"),
    )

    class Meta:
        verbose_name = _("token authorization")
        verbose_name_plural = _("token authorizations")

    def __str__(self):
        return self.contact_person

    def save(self, *args, **kwargs):
        if not self.token:
            existing_tokens = TokenAuth.objects.values_list("token", flat=True)
            self.token = get_token(existing_tokens=existing_tokens)

        return super().save(*args, **kwargs)
