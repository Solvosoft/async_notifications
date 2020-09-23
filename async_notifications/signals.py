# encoding: utf-8
from __future__ import unicode_literals

'''
Created on 21/12/2015

@author: luisza
'''
from django.db.models.signals import post_save, post_delete
from async_notifications.models import EmailNotification, NewsLetterTemplate, NewsLetterTask
from django.dispatch.dispatcher import receiver
from async_notifications.tasks import send_email, task_send_newsletter
import os
import importlib
from django.conf import settings

app = importlib.import_module(settings.CELERY_MODULE).app

@receiver(post_save, sender=EmailNotification)
def check_email(sender, **kwargs):
    obj = kwargs['instance']

    if kwargs['created'] and obj.enqueued is False:
        send_email.delay(obj.pk)


@receiver(post_save, sender=NewsLetterTask)
def add_newsletter_task(sender, **kwargs):
    obj = kwargs['instance']
    if obj.task_id:
        app.control.revoke(obj.task_id, terminate=True)
    t = task_send_newsletter.apply_async(args=(obj.template_id, ), eta=obj.send_date)
    obj.__class__.objects.filter(pk=obj.pk).update(task_id=t.id)


@receiver(post_delete, sender=NewsLetterTask)
def del_newsletter_task(sender, **kwargs):
    obj = kwargs['instance']
    if obj.task_id:
        app.control.revoke(obj.task_id, terminate=True)
