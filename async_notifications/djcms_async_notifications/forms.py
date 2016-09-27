# encoding: utf-8

'''
Free as freedom will be 26/9/2016

@author: luisza
'''

from __future__ import unicode_literals

from async_notifications.widgets import EmailLookup
from async_notifications.models import EmailTemplate
from django import forms

Textarea = forms.widgets.Textarea


class NotificationForm(forms.Form):
    template = forms.ModelChoiceField(queryset=EmailTemplate.objects.all())
    recipient = EmailLookup('emails')
    extra_message = forms.CharField(
        widget=Textarea, required=False)

    uri = forms.CharField(widget=forms.HiddenInput)
    name = forms.CharField(widget=forms.HiddenInput)
    pk = forms.CharField(widget=forms.HiddenInput)
