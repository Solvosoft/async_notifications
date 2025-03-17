# encoding: utf-8

"""
Free as freedom will be 25/9/2016

@author: luisza
"""
from django.forms import SelectMultiple
from djgentelella.widgets.tagging import RemoteAutocompleteEmailTagifyWidget


class BaseAutocomplete:
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["url"] = self.base_url
        return context

    def optgroups(self, name, value, attrs=None):
        if value and value != [""]:
            self.choices.queryset = self.choices.queryset.filter(pk__in=value)
        else:
            self.choices.queryset = self.choices.queryset.none()
        return super().optgroups(name, value, attrs=attrs)


class EmailLookup(BaseAutocomplete, SelectMultiple):
    widget = RemoteAutocompleteEmailTagifyWidget
