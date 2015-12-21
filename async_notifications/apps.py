from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class NotificationsConfig(AppConfig):
    name = 'async_notifications'
    verbose_name = _("Email Notification")

    def ready(self):
        import async_notifications.signals
