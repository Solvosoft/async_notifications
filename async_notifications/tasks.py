# encoding: utf-8
from __future__ import unicode_literals

'''
Created on 20/12/2015

@author: luisza
'''

from .models import EmailNotification
from django.core import mail
from django.conf import settings
import importlib

app = importlib.import_module(settings.CELERY_MODULE).app

@app.task
def send_email(obj):
    """
    Envía un correo 
    obj puede ser un pk o una instancia EmailNotification
    """
    if not isinstance(obj, EmailNotification):
        try:
            obj = EmailNotification.objects.get(pk=obj)
        except:
            return

    send_ok = False
    with mail.get_connection() as connection:
        message = mail.EmailMessage(obj.subject, obj.message,
                                    settings.DEFAULT_FROM_EMAIL,
                                    obj.recipient.split(","),
                                    connection=connection
                                    )
        message.content_subtype = "html" 
        if obj.file:
            message.attach_file(settings.MEDIA_ROOT + obj.file.name)
        try:
            message.send()
            send_ok = True
        except:
            obj.problems = True
            obj.save()

    if send_ok:
        obj.sended = True
        obj.queued = False
        obj.problems = False
        obj.save()


@app.task
def send_daily():
    for email in EmailNotification.objects.filter(sended=False, enqueued=True):
        send_email(email)
