# encoding: utf-8
from __future__ import unicode_literals

import json

'''
Created on 20/12/2015

@author: luisza
'''

from django.template import Context, Template
from .models import EmailTemplate, EmailNotification
from django.apps import apps
from django.template.exceptions import TemplateDoesNotExist
import six


def hexify(text):
    return "".join([str(hex(ord(x))).replace("0x", "") for x in text])


def unhexify(text):
    if "@" in text:
        return text
    return "".join([chr(int(text[x] + text[x + 1], base=16))
                    for x in range(0, len(text), 2)])

def _get_template(code):
    template = None
    if type(code) == six.text_type or type(code) == six.binary_type:
        code = [code]
    for _code in code:
        template = EmailTemplate.objects.filter(code=_code).first()
        if template:
            break
    if template is None:
        raise TemplateDoesNotExist()
    return template


def send_email_from_template(code, recipient,
                             context={},
                             enqueued=True,
                             user=None,
                             upfile=None):


    template = _get_template(code)
    if user is not None:
        context['user'] = user

    if type(recipient) is list or type(recipient) is tuple:
        recipient = ",".join(recipient)

    subject = Template(template.subject)
    message = Template(template.message)
    c = Context(context)
    email = EmailNotification(subject=subject.render(c),
                              message=message.render(c),
                              recipient=recipient,
                              enqueued=enqueued
                              )
    if user is not None:
        email.user = user
    if upfile is not None:
        email.file = upfile

    email.save()


def extract_emails(text):
    if type(text) == str:
        mail_list = text.replace(
            "[", "").replace("]", "").replace("'", "").split(",")
    else:
        mail_list = text

    emails = [unhexify(x.strip()) for x in mail_list]
    return emails


def custom_extract_emails(text):
    if type(text) == str:
        mail_dict = json.loads(text)
    else:
        mail_dict = text
    return mail_dict


def custom_send_email_from_template(code, recipient,
                             context={},
                             enqueued=True,
                             user=None,
                             upfile=None):


    template = _get_template(code)
    if user is not None:
        context['user'] = user

    recipient_json = json.dumps(recipient)
    recipient = recipient_json

    subject = Template(template.subject)
    message = Template(template.message)
    c = Context(context)

    email = EmailNotification(subject=subject.render(c),
                              message=message.render(c),
                              recipient=recipient,
                              enqueued=enqueued
                              )
    if user is not None:
        email.user = user
    if upfile is not None:
        email.file = upfile

    email.save()



def get_model(model_name):
    app_name, model = model_name.split(".")
    return apps.get_model(app_name, model)
