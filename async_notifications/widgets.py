# encoding: utf-8

'''
Free as freedom will be 25/9/2016

@author: luisza
'''


#from ajax_select.fields import (AutoCompleteSelectMultipleField,
#                                AutoCompleteSelectMultipleWidget)
#from django.core.exceptions import ValidationError
from django.forms import Widget, SelectMultiple, forms


class SelectTagifyWidget(Widget):
    template_name='widgets/tagifyselect.html'

    def build_attrs(self, base_attrs, extra_attrs=None):
        """Build an attribute dictionary."""
        dev = {**base_attrs, **(extra_attrs or {})}
        dev['data-url']=self.base_url
        dev['data-widget'] = 'TagifySelect'
        return dev

    @classmethod
    def newwidget(cls, url):
        widget = type('SelectTagifyWidget', cls.__bases__, dict(cls.__dict__))
        widget.base_url = url
        return widget

    @property
    def media(self):
        return forms.Media(css={'all': ('https://cdn.jsdelivr.net/npm/@yaireo/tagify/dist/tagify.css',)},
                           js=('https://cdn.jsdelivr.net/npm/@yaireo/tagify',
                               'https://cdn.jsdelivr.net/npm/@yaireo/tagify/dist/tagify.polyfills.min.js',
                               'async_notifications/tagify.js'))

class BaseAutocomplete:
    def get_context(self, name, value, attrs):
        context = super().get_context(name,value,attrs)
        context['url'] = self.base_url
        return context

    def optgroups(self, name, value, attrs=None):
        if value and value != ['']:
            self.choices.queryset = self.choices.queryset.filter(pk__in=value)
        else:
            self.choices.queryset = self.choices.queryset.none()
        return super().optgroups(name, value, attrs=attrs)


class EmailLookup(BaseAutocomplete, SelectMultiple):
    widget = SelectTagifyWidget


"""
class EmailLookupWidget(AutoCompleteSelectMultipleWidget):

    def value_from_datadict(self, data, files, name):
        # eg. 'members': ['|229|4688|190|']
        # backward compatibility ['1,3,4']
        ids = data.get(name, '')
        if "," in ids:
            return [val for val in ids.split(',') if val]

        return super(EmailLookupWidget, self).value_from_datadict(
            data, files, name)


class EmailLookup(AutoCompleteSelectMultipleField):
    def clean(self, value):
        if not value and self.required:
            raise ValidationError(self.error_messages['required'])
        if not value:
            return None
        return value  # a list of primary keys from widget value_from_datadict

"""
