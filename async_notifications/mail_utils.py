# encoding: utf-8

'''
Free as freedom will be 26/9/2016

@author: luisza
'''

from __future__ import unicode_literals
from .utils import extract_emails, get_model
from .settings import NOTIFICATION_USER_MODEL
#from django.contrib.auth.models import User, Group
User = get_model(NOTIFICATION_USER_MODEL)


def get_mails_from_group(group_name):
    name = group_name.replace("@group", "").replace("__", " ")
    users = User.objects.filter(groups__name=name)

    return[u.email for u in users]


def get_all_emails(text):
    if "@" in text:
        return text.split(",")

    mails = extract_emails(text)
    gmails = []
    for mail in mails:
        if "@group" in mail:
            mails.remove(mail)
            gmails += get_mails_from_group(mail)
    mails += gmails

    return set(mails)
