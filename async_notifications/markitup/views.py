from django.core.handlers.exception import get_exception_response
from django.http import HttpResponse
from async_notifications.newsletter_utils import get_data, render_template_newsletter
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



def preview_newsletter(request):
    templateid = get_template_cookie_value(request)
    data = get_data(templateid, request.POST.get('data', ''))

    dev = render_template_newsletter(data)
        #response= get_exception_response(request, get_resolver(get_urlconf()), 500, e)
        #response.status_code = 200
        #return response
    return HttpResponse(dev)