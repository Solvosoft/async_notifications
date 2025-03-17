# encoding: utf-8

"""
Free as freedom will be 26/9/2016

@author: luisza
"""

import json

from django.core.exceptions import ImproperlyConfigured
from django.template.loader import render_to_string

from .models import TemplateContext, EmailTemplate


class DummyContextObject(object):
    def __init__(self, name):
        self.parent = name

    def __getattr__(self, name):
        return DummyContextObject("%s.%s" % (self.parent, name))

    def __str__(self, *args, **kwargs):
        return "{{ %s }}" % (self.parent)

    def __repr__(self, *args, **kwargs):
        return "{{ %s }}" % (self.parent)


codes = []


def update_template_context_utils(
    code=None, subject=None, context=None, message=None, as_template=False
):
    view_name = subject
    if code is None:
        raise ImproperlyConfigured("Code is required")
    if message is None:
        message = " "
    if as_template:
        new_context = {}
        for c in context:
            if not isinstance(c, str):
                c = c[0]
            new_context[c] = DummyContextObject(c)
        message = render_to_string(message, context=new_context)
    ncode = "%s.%s" % (code, view_name)

    if ncode not in codes:
        temp_context, created = TemplateContext.objects.get_or_create(code=code)
        if not EmailTemplate.objects.filter(code=code).exists():
            EmailTemplate.objects.create(code=code, subject=view_name, message=message)

        if temp_context.context_dic:
            context_dic = json.loads(temp_context.context_dic)
        else:
            context_dic = {}

        if view_name not in context_dic:
            context_dic[view_name] = context
            temp_context.context_dic = json.dumps(context_dic)
            temp_context.save()
            codes.append("%s.%s" % (code, view_name))
