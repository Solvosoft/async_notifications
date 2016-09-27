# encoding: utf-8

'''
Free as freedom will be 26/9/2016

@author: luisza
'''

from __future__ import unicode_literals
from classytags.core import Options
from classytags.helpers import Tag
from classytags.arguments import Argument
from django import template
from django.template.loader import render_to_string

from async_notifications.djcms_async_notifications.forms import NotificationForm
from async_notifications.djcms_async_notifications.utils import (
    get_app_name_models, get_base64url)


register = template.Library()


class Render_email_notification(Tag):
    name = 'render_email_notification'
    options = Options(
        Argument('page', required=True),
    )

    def render_tag(self, context, page):
        if 'request' not in context:
            return ""
        else:
            request = context['request']
            user = request.user

        if not user.is_superuser:
            return ""

        name = get_app_name_models(page)

        uri = request.build_absolute_uri()
        uri = get_base64url(uri)
        return render_to_string(
            'djcms_async_notifications/page_email.html',
            {'request': request,
             'uri': uri,
             'name': name,
             'pk': page.pk},
            request=request
        )

register.tag(Render_email_notification)
