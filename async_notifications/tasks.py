# encoding: utf-8
'''
Created on 20/12/2015

@author: luisza
'''

from __future__ import unicode_literals

from django.conf import settings
from django.core import mail
import importlib
import os

from .mail_utils import get_all_emails
from .models import EmailNotification
from .newsletter_utils import task_send_newsletter_fnc
from .settings import MAX_PER_MAIL, SEND_ONLY_EMAIL, SMTP_DEBUG

app = importlib.import_module(settings.CELERY_MODULE).app


def _send_email(obj, mails, bcc=None, cc=None):
    send_ok = False
    sent = 0
    with mail.get_connection() as connection:
        if SMTP_DEBUG:
            connection.connection.set_debuglevel(1)
        message = mail.EmailMessage(obj.subject, obj.message,
                                    settings.DEFAULT_FROM_EMAIL,
                                    mails,
                                    bcc=bcc,
                                    cc=cc,
                                    connection=connection
                                    )
        message.content_subtype = "html"
        if obj.file:
            if os.path.isfile(settings.MEDIA_ROOT + obj.file.name):
                message.attach_file(settings.MEDIA_ROOT + obj.file.name)
        try:
            message.send(fail_silently=False)
            send_ok = True
            sent+=1
        except Exception as e:
            obj.problems = True
            obj.save()
            print(e)

    if send_ok:
        obj.sent = True
        obj.enqueued = False
        obj.problems = False
        obj.save()
    return sent

@app.task
def send_email(obj):
    """
    Envía un correo 
    obj puede ser un pk o una instancia EmailNotification
    """
    sent=0
    if not isinstance(obj, EmailNotification):
        try:
            obj = EmailNotification.objects.get(pk=obj)
        except:
            return
    if SEND_ONLY_EMAIL:
        mails = SEND_ONLY_EMAIL
        bcc=None
        cc=None
    else:
        mails = list(get_all_emails(obj.recipient))
        bcc = list(get_all_emails(obj.bcc))
        cc = list(get_all_emails(obj.cc))
    while len(mails) > MAX_PER_MAIL:
        s_mails = mails[:MAX_PER_MAIL]
        mails = mails[MAX_PER_MAIL:]
        sent += _send_email(obj, s_mails, bcc=bcc, cc=cc)
    if len(mails) > 0:
        sent += _send_email(obj, mails, bcc=bcc, cc=cc)

    return sent

@app.task
def send_daily():
    sent = 0
    for email in EmailNotification.objects.filter(sent=False, enqueued=True):
        try:
            sent += send_email(email)
        except Exception as e:
            print(e)
            import traceback
            traceback.print_exc()
    return "sent %d"%(sent,)


@app.task
def task_send_newsletter(pk):
    return task_send_newsletter_fnc(pk)