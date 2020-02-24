# encoding: utf-8
'''
Created on 20/12/2015

@author: luisza
'''

from __future__ import unicode_literals

import os

from django.conf import settings
from django.core import mail
import importlib

from .mail_utils import get_all_emails
from .models import EmailNotification
from .settings import MAX_PER_MAIL


app = importlib.import_module(settings.CELERY_MODULE).app

def _send_email_multi_alternatives(obj, mails):
    send_ok = False
    with mail.get_connection() as connection:
        message = mail.EmailMessage(obj.subject, obj.message,
                                    settings.DEFAULT_FROM_EMAIL,
                                    mails,
                                    connection=connection,
                                    cc=obj.cc_mail,bcc=obj.bcc_mail
                                    )
        message.content_subtype = "html"
        if os.path.isfile(settings.MEDIA_ROOT + obj.file.name):
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

def _send_email(obj, mails):
    send_ok = False
    with mail.get_connection() as connection:
        message = mail.EmailMessage(obj.subject, obj.message,
                                    settings.DEFAULT_FROM_EMAIL,
                                    mails,
                                    connection=connection
                                    )
        message.content_subtype = "html"
        if os.path.isfile(settings.MEDIA_ROOT + obj.file.name):
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

    mails = list(get_all_emails(obj.recipient))
    while len(mails) > MAX_PER_MAIL:
        s_mails = mails[:MAX_PER_MAIL]
        mails = mails[MAX_PER_MAIL:]
        _send_email(obj, s_mails)
    if len(mails) > 0:
        _send_email(obj, mails)


@app.task
def send_daily():
    for email in EmailNotification.objects.filter(sended=False, enqueued=True):
        send_email(email)
