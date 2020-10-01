# encoding: utf-8
from __future__ import unicode_literals
'''
Created on 20/12/2015

@author: luisza
'''

from copy import deepcopy

from .settings import EXTRA_BCC, EXTRA_CC

from django.template import Context, Template
from .models import EmailTemplate, EmailNotification
from django.apps import apps
from django.template.exceptions import TemplateDoesNotExist
import six
from . import settings
from django.utils.module_loading import import_string

NEWS_CONTEXT_ELEMENT = {}
NEWS_BASE_MODELS = {}


def import_klass_news_base_models(data):
    data = deepcopy(data)
    for key in data:
        data[key][2] = import_string(data[key][2])
    return data

NEWS_BASE_MODELS.update(import_klass_news_base_models(settings.NEWS_BASE_MODELS))

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

def register_model(name, kass, depth=2,
                   exclude=[], prefix=""):
    global NEWS_CONTEXT_ELEMENT
    if name not in NEWS_CONTEXT_ELEMENT:
        NEWS_CONTEXT_ELEMENT[name] = []
    NEWS_CONTEXT_ELEMENT[name] += describe_class(kass,depth=depth, prefix=prefix, exclude=exclude)

def get_relation_class(field):
    if not field.is_relation:
        return None, None

    related_name = field.related_name if hasattr(field,'related_name') else field.name
    if related_name is None:
        related_name=field.related_model.__name__.lower()+'_set'
    return field.related_model, related_name

def describe_class(kass, prefix="", separator=".", exclude=[], depth=2, cdepth=0):
    fields=kass._meta.get_fields()
    cdepth += 1
    dev = []
    for field in fields:
        name = prefix + field.name
        relkass, relname = get_relation_class(field)
        if cdepth == depth or relkass is None:
            if name not in exclude:
                dev.append([
                    name,
                    field.verbose_name if hasattr(field, 'verbose_name') else field.name,
                    field.help_text if hasattr(field, 'help_text') else ""
                ])
        else:
            if relname:
                name = prefix+relname
            if relkass:
                dev += describe_class(relkass,
                              prefix=name+separator,
                              separator=separator,
                              exclude=exclude,
                              depth=depth, cdepth=cdepth)
    return dev


def get_newsletter_context(name):
    dev = []
    if name in NEWS_CONTEXT_ELEMENT:
        dev = NEWS_CONTEXT_ELEMENT[name]
    return dev

def register_news_basemodel(modelname, description, kass):
    NEWS_BASE_MODELS[modelname]=(modelname, description, kass)

def get_basemodels_dict():
    dev = []
    for name in NEWS_BASE_MODELS:
        dev.append(
            (name, NEWS_BASE_MODELS[name][1])
        )
    return dev

def get_basemodel_info(name):
    dev = []
    if name in NEWS_BASE_MODELS:
        dev = NEWS_BASE_MODELS[name]
    return dev