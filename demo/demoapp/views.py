from django.contrib import messages
from django.shortcuts import render

from async_notifications.utils import send_email_from_template


# Please register context on async_notifications_context file in the root of your app
def index(request):
    if request.GET.get("notify", None):
        send_email_from_template(
            "yourcode",
            ["test@example.com"],
            context={"fieldname": "hello", "fieldname2": "world"},
            enqueued=True,
            user=None,
            upfile=None,
        )
        messages.info(request, "Notification was sent successfully")
    return render(request, "demoapp/index.html")
