from django.contrib import admin

# Register your models here.
from .models import EmailNotification, EmailTemplate
from async_notifications.tasks import send_email
from django.utils.translation import ugettext_lazy as _


class MyNotification(admin.ModelAdmin):
    fields = (("subject", "enqueued", "sended", "problems"),
              "message", "recipient",
              "file"
              )

    list_display = ("subject", "recipient", "enqueued",
                    "sended", "problems", 'create_datetime')

    actions = ['send_now']
    ordering = ['-create_datetime', 'sended', '-enqueued']

    date_hierarchy = 'create_datetime'

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


admin.site.register(EmailTemplate)
admin.site.register(EmailNotification, MyNotification)
