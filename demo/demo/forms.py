from django import forms

from async_notifications.interfaces import NewsLetterInterface
from async_notifications.models import EmailNotification


class FilterForm(forms.Form):
    sent = forms.BooleanField(required=False)
    recipient = forms.CharField(required=False)

class EmailExampleForm(NewsLetterInterface):
    name = "emailexample"

    form = FilterForm
    model = EmailNotification

    field_map = {
        'exclude': {},
        'filter': {
            'sent': 'sent',
            'recipient': 'recipient__in',
        }
    }