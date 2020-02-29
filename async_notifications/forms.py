# encoding: utf-8

'''
Free as freedom will be 25/9/2016

@author: luisza
'''

from __future__ import unicode_literals
from django import forms
from .models import EmailNotification, EmailTemplate
from .settings import TEXT_AREA_WIDGET
from .widgets import EmailLookup
from django.utils.translation import ugettext_lazy as _
#from ajax_select.fields import AutoCompleteSelectMultipleField


class NotificationForm(forms.ModelForm):
    recipient = EmailLookup('emails', label=_('Recipient list'))
    bcc = EmailLookup('emails', label=_('Bcc Recipient list'))
    cc = EmailLookup('emails', label=_('CC Recipient list'))

    class Meta:
        model = EmailNotification
        fields = ("subject", "enqueued", "sended", "problems",
                  "message", "recipient", 'bcc', 'cc',
                  "file")
        widgets = {
            'message': TEXT_AREA_WIDGET
        }

class TemplateForm(forms.ModelForm):
    bcc = EmailLookup('emails', label=_('Bcc Recipient list'))
    cc = EmailLookup('emails', label=_('CC Recipient list'))

    class Meta:
        model = EmailTemplate
        fields = ('code', 'subject', 'message', 'bcc', 'cc')
        widgets = {
            'message': TEXT_AREA_WIDGET
        }