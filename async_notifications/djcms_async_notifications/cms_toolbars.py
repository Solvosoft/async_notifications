# encoding: utf-8

'''
Free as freedom will be 26/9/2016

@author: luisza
'''

from __future__ import unicode_literals

from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool
from cms.utils.urlutils import admin_reverse

from django.utils.translation import ugettext_lazy as _
from async_notifications.models import EmailNotification


@toolbar_pool.register
class EmailToolbar(CMSToolbar):
    watch_models = [EmailNotification]
    supported_apps = ('djcms_async_notifications', )

    def populate(self):
        user = getattr(self.request, 'user', None)
        try:
            view_name = self.request.resolver_match.view_name
        except AttributeError:
            view_name = None

        if user and view_name:
            menu = self.toolbar.get_or_create_menu(
                'async-notification-app', _("Email"))
            change_email_perm = user.has_perm(
                'async_notifications.change_emailnotification')
            add_email_perm = user.has_perm(
                'async_notifications.add_emailnotification')

            change_template_perm = user.has_perm(
                'async_notifications.change_emailtemplate')
            add_template_perm = user.has_perm(
                'async_notifications.add_emailtemplate')

            if add_email_perm:
                url = admin_reverse(
                    'async_notifications_emailnotification_add')
                menu.add_sideframe_item(_('Write email'), url=url)

            if change_email_perm:
                url = admin_reverse(
                    'async_notifications_emailnotification_changelist')
                menu.add_sideframe_item(_('Email list'), url=url)

            menu.add_break()

            if change_template_perm:
                url = admin_reverse(
                    'async_notifications_emailtemplate_changelist')
                menu.add_sideframe_item(_('Email template list'), url=url)

            if add_template_perm:
                url = admin_reverse(
                    'async_notifications_emailtemplate_add')
                menu.add_sideframe_item(_('Write template email'), url=url)