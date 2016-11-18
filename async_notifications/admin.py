from django.contrib import admin
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
import json

from async_notifications.tasks import send_email

from .forms import NotificationForm
from .models import EmailNotification, EmailTemplate, TemplateContext
from .settings import TEXT_AREA_WIDGET
from .utils import extract_emails


class UserAdminListFilter(admin.SimpleListFilter):
    title = _('User')
    parameter_name = 'userf'

    def lookups(self, request, model_admin):
        return (
            ('0', _('All mails')),
            ('1', _('My mails')),
        )

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(user=request.user)
        return queryset

# Register your models here.
#from ckeditor.widgets import CKEditorWidget


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
        if not request.user.is_superuser:
            query = query.filter(user=request.user)
        return query

    def get_list_filter(self, request):
        filter = super(MyNotification, self).get_list_filter(request)
        if request.user.is_superuser:
            return [UserAdminListFilter]
        return filter

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
