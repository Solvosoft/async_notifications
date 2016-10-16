# encoding: utf-8

'''
Free as freedom will be 26/9/2016

@author: luisza
'''

from __future__ import unicode_literals

from .models import TemplateContext, EmailTemplate
import json

codes = []


def update_template_context(code, view_name,  context):
    """ context :
        [
        (name, help_text),
        ]

    """
    ncode = "%s.%s" % (code, view_name)
    try:  # fail ok if no migrations first python manage.py migrate
        if ncode not in codes:
            temp_context, created = TemplateContext.objects.get_or_create(
                code=code)
            try:
                EmailTemplate.objects.get(code=code)
            except:
                EmailTemplate.objects.create(
                    code=code, subject=view_name, message=" ")

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
