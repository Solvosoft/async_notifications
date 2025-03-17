"""
Created on 21/12/2015

@author: luisza
"""

import importlib

from django.conf import settings
from django.db.models.signals import post_save, post_delete, post_migrate
from django.dispatch.dispatcher import receiver


from async_notifications.models import EmailNotification, NewsLetterTask
from async_notifications.tasks import send_email, task_send_newsletter

app = importlib.import_module(settings.CELERY_MODULE).app


@receiver(post_save, sender=EmailNotification)
def check_email(sender, **kwargs):
    obj = kwargs["instance"]

    if kwargs["created"] and obj.enqueued is False:
        send_email.delay(obj.pk)


def add_newsletter_task(sender, **kwargs):
    obj = kwargs["instance"]
    if obj.task_id:
        app.control.revoke(obj.task_id, terminate=True)
    t = task_send_newsletter.apply_async(args=(obj.template_id,), eta=obj.send_date)
    obj.__class__.objects.filter(pk=obj.pk).update(task_id=t.id)


def del_newsletter_task(sender, **kwargs):
    obj = kwargs["instance"]
    if obj.task_id:
        app.control.revoke(obj.task_id, terminate=True)


class LoadContext:
    def try_import(self, app, name="async_notifications_context"):
        dev = None
        try:
            dev = __import__(app + "." + name)
            if dev:
                dev = getattr(dev, name)
        except ModuleNotFoundError as e:
            dev = None
        return dev

    def do_register(self, *args, **kwargs):
        from async_notifications.register import update_template_context_utils

        for app in settings.INSTALLED_APPS:
            mymodule = self.try_import(app)
            if mymodule:
                method_list = [
                    attribute
                    for attribute in dir(mymodule)
                    if callable(getattr(mymodule, attribute))
                    and attribute.startswith("__") is False
                ]
                for method in method_list:
                    context = getattr(mymodule, method)()
                    if isinstance(context, (list, tuple)):
                        for data in context:
                            update_template_context_utils(**data)
                    else:
                        update_template_context_utils(**context)


def load_code_contexts(*args, **kwargs):
    obj = LoadContext()
    obj.do_register()
