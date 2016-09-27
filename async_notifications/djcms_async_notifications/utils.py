# encoding: utf-8

'''
Free as freedom will be 26/9/2016

@author: luisza
'''

from __future__ import unicode_literals
import base64


def get_app_name_models(model):
    return "{0}.{1}".format(model._meta.app_label, model._meta.object_name).lower()


def get_base64url(url):
    return base64.b64encode(str.encode(url))


def get_str_base64url(url):
    return base64.b64decode(str.encode(url))
