# encoding: utf-8
from __future__ import unicode_literals

'''
Created on 21/12/2015

@author: luisza
'''
from django.db.models.signals import post_save
from async_notifications.models import EmailNotification
from django.dispatch.dispatcher import receiver
from async_notifications.tasks import send_email


@receiver(post_save, sender=EmailNotification)
def check_email(sender, **kwargs):
    obj = kwargs['instance']

    if kwargs['created'] and  obj.enqueued is False:
        send_email.delay(obj.pk)