from django.db import models

from django.conf import settings
# Create your models here.
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _


class EmailNotification(models.Model):
    subject = models.CharField(max_length=500, verbose_name=_("Subject"))
    message = models.TextField(verbose_name=_("Message"))
    # coma separated
    recipient = models.TextField(verbose_name=_("Recipient list"))
    enqueued = models.BooleanField(default=True,
                                   verbose_name=_("Enqueued"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                             blank=True, verbose_name=_("User"), on_delete=models.CASCADE)
    sent = models.BooleanField(default=False, verbose_name=_("Sent"))
    file = models.FileField(upload_to='email/%Y/%M', null=True,
                            blank=True, verbose_name=_("File"))
    problems = models.BooleanField(default=False, verbose_name=_("Problems"))
    create_datetime = models.DateTimeField(auto_now_add=True,
                                           verbose_name=_("Create datetime"))

    bcc = models.TextField(verbose_name=_("Bcc Blind carbon copy list"), null=True, blank=True)
    cc = models.TextField(verbose_name=_("Cc Carbon Copy list"), null=True, blank=True)

    def __str__(self):
        return "(%s) %s" % (_("sent") if self.sent else _("Not sent"),
                            self.subject)

    class Meta:
        verbose_name = _("Email notification")
        verbose_name_plural = _("Email notifications")



class EmailTemplate(models.Model):
    code = models.CharField(max_length=50, verbose_name=_("Code"))
    subject = models.CharField(max_length=500, verbose_name=_("Subject"))
    message = models.TextField(verbose_name=_("Message"))
    bcc = models.TextField(verbose_name=_("Bcc Blind carbon copy list"), null=True, blank=True)
    cc = models.TextField(verbose_name=_("Cc Carbon Copy list"), null=True, blank=True)

    def __str__(self):
        return "(%s) %s" % (self.code, self.subject)

    class Meta:
        verbose_name = _("Email template")
        verbose_name_plural = _("Email templates")



class TemplateContext(models.Model):
    code = models.CharField(max_length=50, verbose_name=_("Code"))
    context_dic = models.TextField(verbose_name=_("Context dictionary"))

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = _("Context of template")
        verbose_name_plural = _("Context of template")


class NewsLetterTemplate(models.Model):
    title = models.CharField(max_length=250, unique=True, verbose_name=_("Template title"))
    name = models.SlugField(max_length=250, unique=True, verbose_name=_("Template name"),
                            help_text=_("Name used to save template in template system, used to extends"))
    message = models.TextField(verbose_name=_("Message"),
                               help_text=mark_safe('''<a target="_blank" href="https://docs.djangoproject.com/en/3.0/ref/templates/language/">Referencia a lenguaje de plantillas</a>
                               <br> Puede hacer uso de otras plantillas usando herencia de la forma {% extends 'async_notifications/newslettertemplate name.html' %}
                               <br> Osea el name de este modelo es usado para crear plantillas en disco, por lo que pueden usarse para extender.
                               <br> Recuerde que extends solo puede usarse al inicio de message
                               <br><strong>Nota: </strong> al usar ASYNC_TEMPLATES_NOTIFICATION en settings se modifica el prefijo de la plantilla (posiblemente eliminando async_notifications/)'''))
    model_base = models.CharField(max_length=150, verbose_name=_("Model base"),
                                  help_text=_("Use this model as base for news"))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("News Letter base template")
        verbose_name_plural = _("News Letter base templates")


class NewsLetter(models.Model):
    template = models.ForeignKey(NewsLetterTemplate, on_delete=models.CASCADE)
    subject = models.CharField(max_length=500, verbose_name=_("Subject"))
    message = models.TextField(verbose_name=_("Message"))
    recipient = models.TextField(verbose_name=_("Recipient list"))
    bcc = models.TextField(verbose_name=_("Bcc Blind carbon copy list"), null=True, blank=True)
    cc = models.TextField(verbose_name=_("Cc Carbon Copy list"), null=True, blank=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,  verbose_name=_("Creator"), on_delete=models.CASCADE)
    file = models.FileField(upload_to='email/%Y/%M', null=True,
                            blank=True, verbose_name=_("File"))
    create_datetime = models.DateTimeField(auto_now_add=True,
                                           verbose_name=_("Create datetime"))
    filters = models.CharField(max_length=500, verbose_name=_("Form filters"), null=True, blank=True)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = _("News Letter template")
        verbose_name_plural = _("News Letter templates")


class NewsLetterTask(models.Model):
    template = models.ForeignKey(NewsLetter, on_delete=models.CASCADE)
    send_date = models.DateTimeField(verbose_name=_("Send date"))
    sent = models.BooleanField(default=False, verbose_name=_("Sent"))
    total_sent = models.SmallIntegerField(default=0)
    task_id = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return "%s (%s)"%( self.send_date.strftime("%m/%d/%Y, %H:%M:%S"),
        _('Sent') if self.sent else _("Enqueue"))

    class Meta:
        verbose_name = _("News Letter template")
        verbose_name_plural = _("News Letter templates")