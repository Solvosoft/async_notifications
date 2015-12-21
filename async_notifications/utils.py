# encoding: utf-8
from __future__ import unicode_literals

'''
Created on 20/12/2015

@author: luisza
'''

from django.template import Context, Template
from .models import EmailTemplate, EmailNotification


def send_email_from_template(code, recipient,
                             context={},
                             enqueued=True,
                             user=None,
                             upfile=None):

    template = EmailTemplate.objects.get(code=code)

    if user is not None:
        context['user'] = user

    if type(recipient) is list or type(recipient) is tuple:
        recipient = ",".join(recipient)

    subject = Template(template.subject)
    message = Template(template.message)
    c = Context(context)
    email = EmailNotification(subject=subject.render(c),
                              message=message.render(c),
                              recipient=recipient,
                              enqueued=enqueued
                              )
    if user is not None:
        email.user = user
    if upfile is not None:
        email.file = upfile

    email.save()
