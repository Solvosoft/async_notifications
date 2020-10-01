# encoding: utf-8

'''
Free as freedom will be 25/9/2016

@author: luisza
'''

from __future__ import unicode_literals
from django import forms


from .models import EmailNotification, EmailTemplate, NewsLetter, NewsLetterTemplate
from .settings import TEXT_AREA_WIDGET, NEWSLETTER_WIDGET
from .utils import get_basemodels_dict
from .widgets import EmailLookup
from django.utils.translation import ugettext_lazy as _
#from ajax_select.fields import AutoCompleteSelectMultipleField


class NotificationForm(forms.ModelForm):
    recipient = EmailLookup('emails', label=_('Recipient list'))
    bcc = EmailLookup('emails', label=_('Bcc Recipient list'), required=False)
    cc = EmailLookup('emails', label=_('CC Recipient list'), required=False)

    class Meta:
        model = EmailNotification
        fields = ("subject", "enqueued", "sent", "problems",
                  "message", "recipient", 'bcc', 'cc',
                  "file")
        widgets = {
            'message': TEXT_AREA_WIDGET
        }


class TemplateForm(forms.ModelForm):
    bcc = EmailLookup('emails', label=_('Bcc Recipient list'), required=False)
    cc = EmailLookup('emails', label=_('CC Recipient list'), required=False)

    class Meta:
        model = EmailTemplate
        fields = ('code', 'subject', 'message', 'bcc', 'cc')
        widgets = {
            'message': TEXT_AREA_WIDGET
        }


class NewsLetterForm(forms.ModelForm):

    class Meta:
        model = NewsLetter
        fields = ('template', 'subject', 'message', 'file',
                  'recipient', 'bcc', 'cc', 'filters')
        widgets = {
            'message': NEWSLETTER_WIDGET
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