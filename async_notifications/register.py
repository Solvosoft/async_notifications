# encoding: utf-8

'''
Free as freedom will be 26/9/2016

@author: luisza
'''

from __future__ import unicode_literals

from .models import TemplateContext, EmailTemplate
from django.template.loader import render_to_string
import json

codes = []

class DummyContextObject(object):
    def __init__(self, name):
        self.parent = name

    def __getattr__(self, name):
        return DummyContextObject("%s.%s" % (self.parent, name))

    def __str__(self, *args, **kwargs):
        return "{{ %s }}" % (self.parent)

    def __repr__(self, *args, **kwargs):
        return "{{ %s }}" % (self.parent)


def update_template_context(code, view_name,  context, message=" ", as_template=False):
    """ context :
        [
        (name, help_text),
        ]

    """
    if as_template:
        new_context = {}
        for c in context:
            if not isinstance(c, str):
                c=c[0]
            new_context[c] = DummyContextObject(c)
        message = render_to_string(message, context=new_context)
    ncode = "%s.%s" % (code, view_name)
    try:  # fail ok if no migrations first python manage.py migrate
        if ncode not in codes:
            temp_context, created = TemplateContext.objects.get_or_create(
                code=code)
            try:
                EmailTemplate.objects.get(code=code)
            except:
                EmailTemplate.objects.create(
                    code=code, subject=view_name, message=message)

            if temp_context.context_dic:
                context_dic = json.loads(temp_context.context_dic)
            else:
                context_dic = {}

            if view_name not in context_dic:
                context_dic[view_name] = context
                temp_context.context_dic = json.dumps(context_dic)
                temp_context.save()
                codes.append("%s.%s" % (code, view_name))
    except:
        pass
