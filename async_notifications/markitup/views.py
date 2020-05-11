from django.core.handlers.exception import get_exception_response
from django.http import HttpResponse
from markitup.markup import filter_func
from django.template import Context, Template
from async_notifications import settings as asettings
from async_notifications.models import NewsLetterTemplate
from django.urls import get_resolver, get_urlconf

from async_notifications.register import DummyContextObject


def get_template_cookie_value(request):
    value = None
    try:
        value = int(request.COOKIES['template'])
        if value == 0:
            value=None
    except Exception as e:
        print(e)
        value = None
    return value

def get_template_name_from_path(path):
    return path.replace(asettings.TEMPLATES_NOTIFICATION, '')

def get_data(request, templateid):
    parent, extends = None, None
    data = request.POST.get('data', '')
    if templateid:
        template=NewsLetterTemplate.objects.filter(pk=templateid).first()
        if template:
            if 'async_notifications' in template.file_path:
                parent = "async_notifications/%s.html"%(template.name)
            else:
                parent = get_template_name_from_path(template.file_path)
    if parent:
        extends = '{% extends "'+parent+'" %}\n\n'
    return (data, extends)

def preview_newsletter(request):
    templateid = get_template_cookie_value(request)
    data, extends = get_data(request, templateid)
    markup = filter_func(data)
    if extends:
        markup = extends+markup
    context = {'membresia':DummyContextObject('membresia')}

    try:
        message = Template(markup)
        c = Context(context)
        dev = message.render(c)
    except Exception as e:
        dev = "Error ocurrido en: %s con el tipo <pre>%s</pre>"%(str(e), str(e.__class__.__name__))
        #response= get_exception_response(request, get_resolver(get_urlconf()), 500, e)
        #response.status_code = 200
        #return response
    return HttpResponse(dev)