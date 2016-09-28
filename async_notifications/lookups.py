# encoding: utf-8

'''
Free as freedom will be 25/9/2016

@author: luisza
'''

from __future__ import unicode_literals

from ajax_select import register, LookupChannel
from django.contrib.auth import get_user_model
from django.db.models.query_utils import Q

from django.utils.translation import ugettext as _
from .utils import hexify, extract_emails, get_model
from .settings import (NOTIFICATION_GROUP_MODEL,
                       NOTIFICATION_USER_MODEL,
                       USER_LOOKUP_FIELDS,
                       GROUP_LOOKUP_FIELDS)

Group = get_model(NOTIFICATION_GROUP_MODEL)
User = get_model(NOTIFICATION_USER_MODEL)


class Person(object):
    email = None
    name = None

    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.pk = hexify(email)

    def __str__(self):
        return "%s (%s)" % (self.name, self.email)


def get_filters(filters, q):
    fields = None
    for f in filters['filter']:
        if fields is None:
            fields = Q(**{f: q})
        else:
            fields |= Q(**{f: q})
    return fields


def get_display(obj, name):
    if "__" in name:
        names = name.split("__")
        objs = getattr(obj, names[0])
        return get_display(objs, "__".join(names[1:]))
    nname = getattr(obj, name)
    if callable(nname):
        nname = nname()
    return nname


@register('emails')
class NotificationEmailLookup(LookupChannel):
    model = User

    def get_query_groups(self, q, request):
        fields = get_filters(GROUP_LOOKUP_FIELDS, q)
        groups = Group.objects.filter(fields)
        gs = []
        for g in groups:
            name = get_display(g, GROUP_LOOKUP_FIELDS['display'])
            gs.append(Person(name, "%s@group" % name.replace(" ", "__")))
        return gs

    def get_query_user(self, q, request):

        fields = get_filters(USER_LOOKUP_FIELDS, q)
        users = self.model.objects.filter(
            fields
        ).order_by(USER_LOOKUP_FIELDS['order_by'])[:20]

        persons = [Person(get_display(u, USER_LOOKUP_FIELDS['display']),
                          u.email) for u in users if u.email]
        return persons

    def find_user(self, email):
        r = self.model.objects.filter(email=email)
        if len(r):
            user = r[0]
            return Person(get_display(user, USER_LOOKUP_FIELDS['display']),
                          user.email)
        return

    def find_group(self, email):
        name = email.replace("@group", "").replace("__", " ")
        fields = get_filters(GROUP_LOOKUP_FIELDS, q)
        g = Group.objects.filter(fields)
        if len(g):
            g = g[0]
            name = get_display(g, GROUP_LOOKUP_FIELDS['display'])
            return Person(name,
                          "%s@group" % name.replace(" ", "__")
                          )
        return

    def get_query(self, q, request):
        persons = self.get_query_user(q, request)
        persons += self.get_query_groups(q, request)

        if len(persons) == 0 and "@" in q:
            persons = [Person(_("Add external email"), q)]
        return persons

    def format_item_display(self, item):
        return "<span class='tag'>%s (%s)</span>" % (item.name, item.email)

    def get_objects(self, ids):
        objs = []
        if ids == []:
            return ids
        for email in extract_emails(ids):
            person = self.find_user(email)
            if person is None:
                person = self.find_group(email)
                if person is None:
                    person = Person(_("External user"), email)
            objs.append(person)
        return objs
