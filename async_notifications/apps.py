from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class NotificationsConfig(AppConfig):
    name = 'async_notifications'
    verbose_name = _("Email Notification")
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        import async_notifications.signals
