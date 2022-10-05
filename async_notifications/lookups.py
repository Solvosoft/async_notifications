# encoding: utf-8

'''
Free as freedom will be 25/9/2016

@author: luisza
'''

from django.db.models.query_utils import Q
from django.utils.translation import gettext as _
from .utils import get_model
from .settings import (NOTIFICATION_GROUP_MODEL,
                       NOTIFICATION_USER_MODEL,
                       USER_LOOKUP_FIELDS,
                       GROUP_LOOKUP_FIELDS)

Group = get_model(NOTIFICATION_GROUP_MODEL)
User = get_model(NOTIFICATION_USER_MODEL)


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


class FindEmailsByText:
    model = User

    def find_user(self, email):
        r = self.model.objects.filter(email=email)
        if len(r):
            user = r[0]
            return {'name': get_display(user, USER_LOOKUP_FIELDS['display']), 'value': user.email}
        return

    def find_group(self, email):
        name = email.replace("@group", "").replace("__", " ")
        fields = get_filters(GROUP_LOOKUP_FIELDS, name)
        g = Group.objects.filter(fields)
        if len(g):
            g = g[0]
            name = get_display(g, GROUP_LOOKUP_FIELDS['display'])
            return {'name': name, 'value': "%s@group" % name.replace(" ", "__")}
        return

    def get_query_groups(self, q, request):
        fields = get_filters(GROUP_LOOKUP_FIELDS, q)
        groups = Group.objects.filter(fields)
        gs = []
        for g in groups:
            name = get_display(g, GROUP_LOOKUP_FIELDS['display'])
            gs.append({'name': name, 'value': name.replace(" ", "__")+'@group'})
        return gs

    def get_query_user(self, q, request):
        fields = get_filters(USER_LOOKUP_FIELDS, q)
        users = self.model.objects.filter(
            fields
        ).order_by(USER_LOOKUP_FIELDS['order_by'])[:20]
        persons = [{'name': get_display(u, USER_LOOKUP_FIELDS['display']), 'value': u.email} for u in users if u.email]
        return persons

    def get_query(self, q, request):
        persons = self.get_query_user(q, request)
        persons += self.get_query_groups(q, request)

        if len(persons) == 0 and "@" in q:
            persons = [{'name': _("Add external email"), 'value': q}]
        return persons

