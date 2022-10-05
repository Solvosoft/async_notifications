# encoding: utf-8

'''
Free as freedom will be 25/9/2016

@author: luisza
'''

from __future__ import unicode_literals

from django import forms
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from .models import EmailNotification, EmailTemplate, NewsLetter, NewsLetterTemplate
from .settings import TEXT_AREA_WIDGET, NEWSLETTER_WIDGET
from .utils import get_basemodels_dict
from .widgets import EmailLookup, SelectTagifyWidget


#from ajax_select.fields import AutoCompleteSelectMultipleField


class NotificationForm(forms.ModelForm):
    class Meta:
        model = EmailNotification
        fields = ("subject", "enqueued", "sent", "problems",
                  "message", "recipient", 'bcc', 'cc',
                  "file")
        widgets = {
            'message': TEXT_AREA_WIDGET,
            'recipient': SelectTagifyWidget.newwidget(reverse_lazy('async_notifications:api_emails')),
            'bcc': SelectTagifyWidget.newwidget(reverse_lazy('async_notifications:api_emails')),
            'cc': SelectTagifyWidget.newwidget(reverse_lazy('async_notifications:api_emails')),
        }


class TemplateForm(forms.ModelForm):
    class Meta:
        model = EmailTemplate
        fields = ('code', 'subject', 'message', 'bcc', 'cc')
        widgets = {
            'message': TEXT_AREA_WIDGET,
            'bcc': SelectTagifyWidget.newwidget(reverse_lazy('async_notifications:api_emails')),
            'cc': SelectTagifyWidget.newwidget(reverse_lazy('async_notifications:api_emails')),
        }


class NewsLetterForm(forms.ModelForm):

    class Meta:
        model = NewsLetter
        fields = ('template', 'subject', 'message', 'file',
                  'recipient', 'bcc', 'cc', 'filters')
        widgets = {
            'message': NEWSLETTER_WIDGET,
            'recipient': SelectTagifyWidget.newwidget(reverse_lazy('async_notifications:api_emails')),
            'bcc': SelectTagifyWidget.newwidget(reverse_lazy('async_notifications:api_emails')),
            'cc': SelectTagifyWidget.newwidget(reverse_lazy('async_notifications:api_emails')),
        }

    class Media:
        css = {
            'all': ['//cdn.jsdelivr.net/npm/select2@4.0.13/dist/css/select2.min.css']
        }
        js = ['//cdn.jsdelivr.net/npm/select2@4.0.13/dist/js/select2.min.js',
            'async_notifications/previewupdater.js']


class NewsLetterAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        dev = super().__init__(*args, **kwargs)
        self.fields['model_base'] = forms.ChoiceField(
            choices=get_basemodels_dict(),
            widget=forms.Select
        )
        return dev

    class Meta:
        model = NewsLetterTemplate
        fields = '__all__'


class TagifyFormValue(forms.Form):
    value=forms.CharField()
