# encoding: utf-8
from __future__ import unicode_literals

from .settings import EXTRA_BCC, EXTRA_CC

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

def get_bcc_field(template, bcc):
    bcc = bcc or EXTRA_BCC
    if template.cc is not None:
        if bcc is None:
            bcc = template.cc
        else:
            bcc +=","+template.cc
    return bcc

def get_cc_field(template, cc):
    cc = cc or EXTRA_CC
    if template.cc is not None:
        if cc is None:
            cc = template.cc
        else:
            cc +=","+template.cc
    return cc

def send_email_from_template(code, recipient,
                             context={},
                             enqueued=True,
                             user=None,
                             upfile=None,
                             bcc=None,
                             cc=None):

    template = _get_template(code)
    if user is not None:
        context['user'] = user

    if type(recipient) is list or type(recipient) is tuple:
        recipient = ",".join(recipient)

    subject = Template(template.subject)
    message = Template(template.message)
    c = Context(context)
    bcc=get_bcc_field(template, bcc)
    cc=get_cc_field(template, cc)
    email = EmailNotification(subject=subject.render(c),
                              message=message.render(c),
                              recipient=recipient,
                              enqueued=enqueued,
                              bcc=bcc,
                              cc=cc
                              )
    if user is not None:
        email.user = user
    if upfile is not None:
        email.file = upfile

    email.save()


def extract_emails(text):
    if isinstance(text, str):
        mail_list = text.replace(
            "[", "").replace("]", "").replace("'", "").split(",")
    else:
        mail_list = text
        mail_list = [x.replace('[', '').replace(']', '').replace("'", '') for x in mail_list ]
    emails = [unhexify(x.strip()) for x in mail_list]
    return emails


def get_model(model_name):
    app_name, model = model_name.split(".")
    return apps.get_model(app_name, model)
