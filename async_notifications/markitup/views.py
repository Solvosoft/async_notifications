from django.http import HttpResponse

from async_notifications.newsletter_utils import get_data, render_template_newsletter


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
    return HttpResponse(dev)