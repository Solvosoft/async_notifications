from django.apps import AppConfig
from django.db.models.signals import post_migrate, post_delete, post_save
from django.utils.translation import gettext_lazy as _


class NotificationsConfig(AppConfig):
    name = "async_notifications"
    verbose_name = _("Email Notification")
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        from . import signals
        from .models import NewsLetterTask, EmailNotification

        post_save.connect(signals.check_email, sender=EmailNotification)
        post_save.connect(signals.add_newsletter_task, sender=NewsLetterTask)
        post_delete.connect(signals.del_newsletter_task, sender=NewsLetterTask)
        post_migrate.connect(signals.load_code_contexts, sender=self)
