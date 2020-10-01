from django.contrib import admin
from django.db import models
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
import json
import os
from async_notifications.tasks import send_email, task_send_newsletter
from django.conf import settings
from .forms import NotificationForm, TemplateForm, NewsLetterForm, NewsLetterAdminForm
from .models import EmailNotification, EmailTemplate, TemplateContext, NewsLetterTask, NewsLetter, NewsLetterTemplate
from .settings import TEXT_AREA_WIDGET, NEWS_CONTEXT_INSTANCE
from .utils import extract_emails, register_model, get_newsletter_context


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

    fields = (("enqueued", "sent", "problems"),
              "subject",
              "recipient", "bcc", 'cc',
              "message",
              "file"
              )

    list_display = ("subject", "recipient_emails", "enqueued",
                    "sent", "problems", 'create_datetime')
    search_fields = ('subject', 'message__icontains')

    readonly_fields = ['recipient_emails']
    actions = ['send_now']
    ordering = ['-create_datetime', 'sent', '-enqueued']

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
    field = ('code', 'subject', 'message', 'template_context')
    list_display = ('code', 'subject')
    search_fields = ['code', 'subject']
    readonly_fields = ['template_context']
    form = TemplateForm

    def template_context(self, obj=None):
        if obj is None:
            return ""
        try:
            tcontext = TemplateContext.objects.get(code=obj.code)
            context = json.loads(tcontext.context_dic)
        except TemplateContext.DoesNotExist as e:
            if settings.DEBUG:
                return obj.code+" -- "+str(e)
            return ""
        dev = ""
        for view_name in context:
             
            dev += "<h4>%s</h4><ol>" % (view_name)
            datacont = context[view_name]
            if isinstance(datacont, dict):
                datacont = datacont.items()
            for name, help_text in datacont:
                dev += "<li><strong>%s:</strong> %s</li><br>" % (name, help_text)
            dev += "</ol>"
 
        return mark_safe(dev)
    template_context.short_description = _("Template context")


class NewsTask(admin.TabularInline):
    model = NewsLetterTask
    extra = 1
    fields = ['send_date']


class NewsLetterAdmin(admin.ModelAdmin):
    inlines = [NewsTask]
    form=NewsLetterForm
    list_display = ('subject', 'template',)
    fieldsets = (
        (None, {
            'fields': ('template', 'subject', 'message', 'file')
        }),
        ('Recipients', {
            'classes': ('collapse', ),
            'fields': ('recipient',   ),#'bcc', 'cc'
        }),
    )
    actions = ['send_newsletter']

    def send_newsletter(self, request, queryset):
        for obj in queryset:
           #task_send_newsletter(obj.pk)
           task_send_newsletter.delay(obj.pk)

    send_newsletter.short_description = "Send newsletter"

    def save_model(self, request, obj, form, change):
        if not hasattr(obj, 'creator') or obj.creator is None:
            obj.creator = request.user
        return super().save_model(request, obj, form, change)



class NewsLetterTemplateAdmin(admin.ModelAdmin):
    prepopulated_fields = {"name": ("title",)}
    form = NewsLetterAdminForm

admin.site.register(EmailTemplate, EmailTemplateAdmin)
admin.site.register(EmailNotification, MyNotification)
admin.site.register(NewsLetter, NewsLetterAdmin)
admin.site.register(NewsLetterTemplate, NewsLetterTemplateAdmin)

#register_model(EmailNotification)
if settings.DEBUG:
    admin.site.register(TemplateContext)