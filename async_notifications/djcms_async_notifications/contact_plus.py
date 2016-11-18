# encoding: utf-8


'''
Created on 18/11/2016

@author: luisza
'''
from __future__ import unicode_literals

from async_notifications.register import update_template_context
from async_notifications.settings import CONTACT_PLUS_EMAIL
from async_notifications.utils import send_email_from_template


context = [
    ('from_email', 'From email for header'),
    ('context',
        """ {data: form data, ordered_data: form data in order, instance: form plugin}""" ),
    ('subject', "Email subject"),
    ('instance', "form plugin instance"),
    ('headers', "Http headers (don't use)"),
    ('to',  "to email list")
]


def send_email(**kwargs):
    context_name = "contact_plus"
    update_template_context("fromsite_" + context_name,
                            'New contact form submited',
                            context
                            )

    update_template_context("sitetouser_" + context_name,
                            'Answer for contact form submited',
                            context
                            )
    send_email_from_template("fromsite_" + context_name,
                             kwargs['to'],
                             context=kwargs,
                             enqueued=True)

    send_email_from_template("sitetouser_" + context_name,
                             kwargs['context']['data'][CONTACT_PLUS_EMAIL],
                             context=kwargs,
                             enqueued=True)
