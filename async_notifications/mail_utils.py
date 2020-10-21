# encoding: utf-8

'''
Free as freedom will be 26/9/2016

@author: luisza
'''

from __future__ import unicode_literals

from .settings import (NOTIFICATION_USER_MODEL, USER_LOOKUP_FIELDS,
                       NOTIFICATION_GROUP_MODEL, GROUP_LOOKUP_FIELDS)
from .utils import extract_emails, get_model


#from django.contrib.auth.models import User, Group
User = get_model(NOTIFICATION_USER_MODEL)
Group = get_model(NOTIFICATION_GROUP_MODEL)


def get_mails_from_group(group_name):
    name = group_name.replace("@group", "").replace("__", " ")
    group = Group.objects.get(**{GROUP_LOOKUP_FIELDS['group_lookup']: name})
    email = None
    # check if group has email (util with mail list approach)
    name_field = GROUP_LOOKUP_FIELDS['email']

    if name_field:
        if hasattr(group, name_field):
            email = getattr(group, name_field)
    if email:
        return [email]
    if 'group_lookup' in  USER_LOOKUP_FIELDS:
        users = User.objects.filter(**{USER_LOOKUP_FIELDS['group_lookup']: name})
        return [u.email for u in users]
    return []

def get_all_emails(text):
    if text is None:
        return []
    mails = extract_emails(text)
    gmails = []
    for mail in mails:
        if "@group" in mail:
            mails.remove(mail)
            gmails += get_mails_from_group(mail)
    mails += gmails
    return set(mails)
