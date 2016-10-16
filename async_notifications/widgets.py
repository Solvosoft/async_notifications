# encoding: utf-8

'''
Free as freedom will be 25/9/2016

@author: luisza
'''

from __future__ import unicode_literals


from django.forms.widgets import Textarea
from django.template.loader import render_to_string

from ajax_select.fields import (AutoCompleteSelectMultipleField,
                                AutoCompleteSelectMultipleWidget)


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
    pass
