# encoding: utf-8

'''
Free as freedom will be 26/9/2016

@author: luisza
'''

from __future__ import unicode_literals

from django.conf import settings
import importlib
import os

NOTIFICATION_GROUP_MODEL = getattr(
    settings, 'ASYNC_NOTIFICATION_GROUP', 'auth.Group')

GROUP_LOOKUP_FIELDS = getattr(
    settings, 'ASYNC_NOTIFICATION_GROUP_LOOKUP_FIELDS',
    {'order_by': 'name',
     'email': None,
     'display': 'name',
     'group_lookup': 'name',
     'filter': ['name__icontains']})


AUTH_USER = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')
NOTIFICATION_USER_MODEL = getattr(
    settings, 'ASYNC_NOTIFICATION_USER', AUTH_USER)

USER_LOOKUP_FIELDS = getattr(
    settings, 'ASYNC_NOTIFICATION_USER_LOOKUP_FIELDS',
    {'order_by': 'username',
     'display': 'username',
     'filter': ['username__icontains',
                'first_name__icontains',
                'last_name__icontains'],
     'group_lookup': 'groups__name'})


MAX_PER_MAIL = getattr(settings, 'ASYNC_NOTIFICATION_MAX_PER_MAIL', 40)

TEXT_AREA_WIDGET_TXT = getattr(settings, 'ASYNC_NOTIFICATION_TEXT_AREA_WIDGET',
                               'django.forms.widgets.Textarea')
NEWSLETTER_WIDGET = getattr(settings, 'ASYNC_NEWSLETTER_WIDGET',
                               TEXT_AREA_WIDGET_TXT)

module_name, class_name = TEXT_AREA_WIDGET_TXT.rsplit(".", 1)
TEXT_AREA_WIDGET = getattr(importlib.import_module(module_name), class_name)

module_name, class_name = NEWSLETTER_WIDGET.rsplit(".", 1)
NEWSLETTER_WIDGET = getattr(importlib.import_module(module_name), class_name)


CONTACT_PLUS_EMAIL = getattr(
    settings, 'ASYNC_NOTIFICATION_CONTACT_PLUS_EMAIL', 'email')

EXTRA_BCC = getattr(settings, 'ASYNC_BCC', None)
EXTRA_CC = getattr(settings, 'ASYNC_CC', None)
SEND_ONLY_EMAIL = getattr(settings, 'ASYNC_SEND_ONLY_EMAIL', None)
SMTP_DEBUG = getattr(settings, 'ASYNC_SMTP_DEBUG', False)

TEMPLATES_NOTIFICATION = getattr(settings, 'ASYNC_TEMPLATES_NOTIFICATION', None)

if TEMPLATES_NOTIFICATION is None:
    import pkg_resources
    base = pkg_resources.resource_filename('async_notifications', 'templates/async_notifications/base.html')
    TEMPLATES_NOTIFICATION = base.replace('base.html', '')

NEWS_CONTEXT_INSTANCE = None
NEWSLETTER_SEVER_CONFIGS = getattr(settings, 'ASYNC_NEWSLETTER_SEVER_CONFIGS', None)
NEWS_BASE_MODELS = getattr(settings, 'ASYNC_NEWS_BASE_MODELS', {})
NEWSLETTER_HEADER  = getattr(settings, 'ASYNC_NEWSLETTER_HEADER', {})