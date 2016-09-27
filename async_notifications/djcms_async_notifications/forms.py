# encoding: utf-8

'''
Free as freedom will be 26/9/2016

@author: luisza
'''

from __future__ import unicode_literals

from async_notifications.widgets import EmailLookup
from async_notifications.models import EmailTemplate
from django import forms
from django.utils.translation import ugettext_lazy as _

Textarea = forms.widgets.Textarea


class NotificationForm(forms.Form):
    template = forms.ModelChoiceField(queryset=EmailTemplate.objects.all(),
                                      label=_('Template'))
    recipient = EmailLookup('emails', label=_('Recipient list'))
    extra_message = forms.CharField(
        widget=Textarea, required=False, label=_('Extra message'))

    uri = forms.CharField(widget=forms.HiddenInput)
    name = forms.CharField(widget=forms.HiddenInput)
    pk = forms.CharField(widget=forms.HiddenInput)
