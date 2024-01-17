from django.db.models import BigIntegerField, Max, Model
from django.db.models.functions import Cast
from django.utils.translation import gettext_lazy as _

from vng_api_common.exceptions import Conflict


def number_generator(self, model: Model) -> None:
    if not self.nummer:
        max_nummer = (
            model.objects.annotate(
                nummer_int=Cast("nummer", output_field=BigIntegerField())
            ).aggregate(Max("nummer_int"))["nummer_int__max"]
            or 0
        )
        self.nummer = str(max_nummer + 1).rjust(10, "0")
        if len(self.nummer) > 10:
            raise Conflict(
                _(
                    "Er kon niet automatisch een opvolgend nummer worden gegenereerd. "
                    "Het maximaal aantal tekens is bereikt."
                )
            )
