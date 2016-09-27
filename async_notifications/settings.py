# encoding: utf-8

'''
Free as freedom will be 26/9/2016

@author: luisza
'''

from __future__ import unicode_literals
from django.conf import settings
import importlib

NOTIFICATION_GROUP_MODEL = getattr(
    settings, 'ASYNC_NOTIFICATION_GROUP', 'auth.Group')

GROUP_LOOKUP_FIELDS = getattr(
    settings, 'ASYNC_NOTIFICATION_GROUP_LOOKUP_FIELDS',
    {'order_by': 'name',
     'display': 'name',
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
                'last_name__icontains']})


MAX_PER_MAIL = getattr(settings, 'ASYNC_NOTIFICATION_MAX_PER_MAIL', 40)

TEXT_AREA_WIDGET_TXT = getattr(settings, 'ASYNC_NOTIFICATION_TEXT_AREA_WIDGET',
                               'django.forms.widgets.Textarea')


module_name, class_name = TEXT_AREA_WIDGET_TXT.rsplit(".", 1)
TEXT_AREA_WIDGET = getattr(importlib.import_module(module_name), class_name)
