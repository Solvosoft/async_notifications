# encoding: utf-8
from __future__ import unicode_literals

'''
Created on 21/12/2015

@author: luisza
'''
from django.db.models.signals import post_save, post_delete
from async_notifications.models import EmailNotification, NewsLetterTemplate
from django.dispatch.dispatcher import receiver
from async_notifications.tasks import send_email
import os

@receiver(post_save, sender=EmailNotification)
def check_email(sender, **kwargs):
    obj = kwargs['instance']

    if kwargs['created'] and  obj.enqueued is False:
        send_email.delay(obj.pk)

@receiver(post_delete, sender=NewsLetterTemplate)
def delete_file_news(sender, **kwargs):
    instance = kwargs['instance']
    if instance.file_path is None:
        from async_notifications import settings as asettings
        filepath = "%s%s.html" % (asettings.TEMPLATES_NOTIFICATION,
                                  instance.name)
    else:
        filepath = instance.file_path

    if os.path.exists(filepath):
        os.remove(filepath)