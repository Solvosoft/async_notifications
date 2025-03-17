# encoding: utf-8

"""
Free as freedom will be 25/9/2016

@author: luisza
"""


from django import forms
from django.urls import reverse_lazy
from djgentelella.forms.forms import GTForm
from djgentelella.widgets import core as genwidgets
from djgentelella.widgets.tagging import (
    EmailTaggingInput,
    RemoteAutocompleteEmailTagifyWidget,
)

from .models import EmailNotification, EmailTemplate, NewsLetter, NewsLetterTemplate
from .settings import TEXT_AREA_WIDGET, NEWSLETTER_WIDGET
from .utils import get_basemodels_dict


class NotificationForm(GTForm, forms.ModelForm):
    class Meta:
        model = EmailNotification
        fields = (
            "subject",
            "enqueued",
            "sent",
            "problems",
            "message",
            "recipient",
            "bcc",
            "cc",
            "file",
        )
        widgets = {
            "subject": genwidgets.TextInput,
            "enqueued": genwidgets.YesNoInput,
            "sent": genwidgets.YesNoInput,
            "problems": genwidgets.YesNoInput,
            "message": genwidgets.Textarea,
            "recipient": EmailTaggingInput,  # ("async_notifications:contact"),
            "bcc": EmailTaggingInput,  # ("async_notifications:contact"),
            "cc": EmailTaggingInput,  # ("async_notifications:contact"),
            "file": genwidgets.FileInput,
        }


class TemplateForm(GTForm, forms.ModelForm):
    default_render_type = "as_grid"
    grid_representation = [
        [["code"], ["subject"]],
        [["bcc"], ["cc"]],
        [["email_context"]],
        [["message"]],
    ]

    def email_context(self):
        return "Hola"

    class Meta:
        model = EmailTemplate
        fields = ("code", "subject", "message", "bcc", "cc")
        widgets = {
            "code": genwidgets.TextInput,
            "subject": genwidgets.TextInput,
            "message": TEXT_AREA_WIDGET,
            "bcc": RemoteAutocompleteEmailTagifyWidget.newwidget(
                reverse_lazy("async_notifications:email_to_tagify")
            ),
            "cc": RemoteAutocompleteEmailTagifyWidget.newwidget(
                reverse_lazy("async_notifications:email_to_tagify")
            ),
        }


class NewsLetterForm(GTForm, forms.ModelForm):

    class Meta:
        model = NewsLetter
        fields = (
            "template",
            "subject",
            "message",
            "file",
            "recipient",
            "bcc",
            "cc",
            "filters",
        )
        widgets = {
            "message": NEWSLETTER_WIDGET,
            "recipient": RemoteAutocompleteEmailTagifyWidget.newwidget(
                reverse_lazy("async_notifications:email_to_tagify")
            ),
            "bcc": RemoteAutocompleteEmailTagifyWidget.newwidget(
                reverse_lazy("async_notifications:email_to_tagify")
            ),
            "cc": RemoteAutocompleteEmailTagifyWidget.newwidget(
                reverse_lazy("async_notifications:email_to_tagify")
            ),
        }


class NewsLetterTemplateForm(GTForm, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        dev = super().__init__(*args, **kwargs)
        self.fields["model_base"] = forms.ChoiceField(
            choices=get_basemodels_dict(), widget=forms.Select
        )
        return dev

    class Meta:
        model = NewsLetterTemplate
        fields = "__all__"


class NewsLetterTaskForm(GTForm, forms.ModelForm):
    class Meta:
        model = NewsLetter
        fields = "__all__"


class TagifyFormValue(GTForm, forms.Form):
    value = forms.CharField()
