from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from async_notifications.forms import TagifyFormValue
from async_notifications.lookups import FindEmailsByText
from async_notifications.forms import (
    NotificationForm,
    TemplateForm,
    NewsLetterForm,
    NewsLetterTemplateForm,
    NewsLetterTaskForm,
)


@login_required
def email_notification_view(request):
    context = {
        "create_form": NotificationForm(prefix="create"),
        "update_form": NotificationForm(prefix="update"),
    }
    return render(
        request, "async_notifications/email_notification.html", context=context
    )


@login_required
def email_template(request):
    context = {
        "create_form": TemplateForm(prefix="create"),
        "update_form": TemplateForm(prefix="update"),
    }
    return render(request, "async_notifications/email_template.html", context=context)


@login_required
def newsletter(request):
    context = {
        "create_form": NewsLetterForm(prefix="create"),
        "update_form": NewsLetterForm(prefix="update"),
    }
    return render(
        request, "async_notifications/newsletter_template.html", context=context
    )


@login_required
def newsletter_template(request):
    context = {
        "create_form": NewsLetterTemplateForm(prefix="create"),
        "update_form": NewsLetterTemplateForm(prefix="update"),
    }
    return render(
        request, "async_notifications/newsletter_template.html", context=context
    )


@login_required
def newsletter_tasks(request):
    context = {
        "create_form": NewsLetterTaskForm(prefix="create"),
        "update_form": NewsLetterTaskForm(prefix="update"),
    }
    return render(request, "async_notifications/newsletter_task.html", context=context)


@login_required
def email_to_tagify(request):
    form = TagifyFormValue(request.GET)
    form.is_valid()
    value = form.cleaned_data.get("value", "")
    query = []
    if value:
        query = FindEmailsByText().get_query(value, request)
    return JsonResponse(query, safe=False)
