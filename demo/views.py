from django.http import HttpResponse

from async_notifications.register import update_template_context
from async_notifications.utils import send_email_from_template

context = [
    ('fieldname', 'Field description'),
    ('fieldname2', 'Field description'),
]
update_template_context("yourcode",  'your email subject', context)


def index(request):
    send_email_from_template("yourcode", ['test@example.com'],
                             context={
                                 'fieldname': 'hello',
                                 'fieldname2': 'world'
                             },
                             enqueued=True,
                             user=None,
                             upfile=None)
    return HttpResponse("It Works, see admin")