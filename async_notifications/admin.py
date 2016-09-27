from django.contrib import admin

# Register your models here.
from .models import EmailNotification, EmailTemplate, TemplateContext
from async_notifications.tasks import send_email
from django.utils.translation import ugettext_lazy as _
from .forms import NotificationForm
from .utils import extract_emails
import json
from django.utils.safestring import mark_safe

from django.db import models
#from ckeditor.widgets import CKEditorWidget

from .settings import TEXT_AREA_WIDGET


class MyNotification(admin.ModelAdmin):

    formfield_overrides = {
        models.TextField: {'widget': TEXT_AREA_WIDGET}
    }

    fields = (("enqueued", "sended", "problems"),
              "subject",
              "recipient",
              "message",
              "file"
              )

    list_display = ("subject", "recipient_emails", "enqueued",
                    "sended", "problems", 'create_datetime')

    readonly_fields = ['recipient_emails']
    actions = ['send_now']
    ordering = ['-create_datetime', 'sended', '-enqueued']

    date_hierarchy = 'create_datetime'

    form = NotificationForm

    def get_queryset(self, request):
        query = super(MyNotification, self).get_queryset(request)
        return query.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

    def send_now(self, request, queryset):
        for email in queryset:
            send_email.delay(email.pk)
    send_now.short_description = _("Send email now")

    def recipient_emails(self, obj):
        mails = extract_emails(obj.recipient)
        if len(mails) > 5:
            return ", ".join(mails[:5]) + str(_(" and more"))
        return ", ".join(mails)
    recipient_emails.short_description = _("Recipients")


class EmailTemplateAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TEXT_AREA_WIDGET}
    }

    field = ('code', 'subject', 'message', 'template_context')
    readonly_fields = ['template_context']

    def template_context(self, obj=None):
        if obj is None:
            return ""
        try:
            tcontext = TemplateContext.objects.get(code=obj.code)
            context = json.loads(tcontext.context_dic)
        except:
            return ""
        dev = ""
        for view_name in context:
            dev += "<h4>%s</h4><ol>" % (view_name)
            for name, help in context[view_name]:
                dev += "<li><strong>%s:</strong> %s<br></li>" % (name, help)
            dev += "</ol>"
        return mark_safe(dev)
    template_context.short_description = _("Template context")

# admin.site.register(TemplateContext)
admin.site.register(EmailTemplate, EmailTemplateAdmin)
admin.site.register(EmailNotification, MyNotification)
