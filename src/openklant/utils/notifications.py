from typing import Dict, List, Union

from django.db import models, transaction

from notifications_api_common.models import NotificationTypes
from notifications_api_common.tasks import create_failed_notification, send_notification
from notifications_api_common.viewsets import NotificationCreateMixin, NotificationMixin


class MultipleNotificationMixin(NotificationMixin):
    """
    NotificationMixin that adds support for sending notification per object in convenience endpoints.
    """

    notification_fields: dict[str, dict[str, str]]

    def notify(
        self,
        status_code: int,
        data: Union[List, Dict],
        instance: models.Model = None,
        **kwargs,
    ) -> None:
        super().notify(status_code, data, instance)

    def _message(self, data, instance=None):
        for field, config in self.notification_fields.items():
            field_data = data[field]
            notifications = field_data if isinstance(field_data, list) else [field_data]

            for notif in notifications:
                # build the content of the notification
                message = self.construct_message(
                    notif,
                    instance=instance,
                    kanaal=config["notifications_kanaal"],
                    model=config["model"],
                    action=config.get("action"),
                )

                pk = create_failed_notification(message, NotificationTypes.notification)

                transaction.on_commit(
                    lambda msg=message: send_notification.delay(msg, pk)
                )


class MultipleNotificationCreateMixin(
    MultipleNotificationMixin, NotificationCreateMixin
): ...
