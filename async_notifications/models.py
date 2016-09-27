from django.db import models

from django.conf import settings
# Create your models here.
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class EmailNotification(models.Model):
    subject = models.CharField(max_length=500, verbose_name=_("Subject"))
    message = models.TextField(verbose_name=_("Message"))
    # coma separated
    recipient = models.TextField(verbose_name=_("Recipient list"))
    enqueued = models.BooleanField(default=True,
                                   verbose_name=_("Enqueued"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                             blank=True, verbose_name=_("User"))
    sended = models.BooleanField(default=False, verbose_name=_("Sended"))
    file = models.FileField(upload_to='email/%Y/%M', null=True,
                            blank=True, verbose_name=_("File"))
    problems = models.BooleanField(default=False, verbose_name=_("Problems"))
    create_datetime = models.DateTimeField(auto_now_add=True,
                                           verbose_name=_("Create datetime"))

    def __str__(self):
        return "(%s) %s" % (_("sended") if self.sended else _("Not sended"),
                            self.subject)

    class Meta:
        verbose_name = _("Email notification")
        verbose_name_plural = _("Email notifications")


@python_2_unicode_compatible
class EmailTemplate(models.Model):
    code = models.CharField(max_length=50, verbose_name=_("Code"))
    subject = models.CharField(max_length=500, verbose_name=_("Subject"))
    message = models.TextField(verbose_name=_("Message"))

    def __str__(self):
        return "(%s) %s" % (self.code, self.subject)

    class Meta:
        verbose_name = _("Email template")
        verbose_name_plural = _("Email templates")


@python_2_unicode_compatible
class TemplateContext(models.Model):
    code = models.CharField(max_length=50, verbose_name=_("Code"))
    context_dic = models.TextField(verbose_name=_("Context dictionary"))

    class Meta:
        verbose_name = _("Context of template")
        verbose_name_plural = _("Context of template")
