# encoding: utf-8

'''
Free as freedom will be 25/9/2016

@author: luisza
'''

from __future__ import unicode_literals
from ajax_select.fields import (AutoCompleteSelectMultipleField,
                                AutoCompleteSelectMultipleWidget)
from django.core.exceptions import ValidationError


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


