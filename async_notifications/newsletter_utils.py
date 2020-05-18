from django.http import QueryDict

from async_notifications.models import NewsLetter, NewsLetterTask, NewsLetterTemplate
from async_notifications.utils import get_basemodel_info
from async_notifications import settings as asettings
from markitup.markup import filter_func
from django.template import Context, Template
from async_notifications.models import NewsLetterTemplate
from django.core import mail
from .settings import SMTP_DEBUG
from django.conf import settings
import os

def render_template_newsletter(data, extends, context):
    markup = filter_func(data)
    if extends:
        markup = extends+markup
    try:
        message = Template(markup)
        c = Context(context)
        dev = message.render(c)
    except Exception as e:
        dev = "Error ocurrido en: %s con el tipo <pre>%s</pre>"%(str(e), str(e.__class__.__name__))
    return dev

def get_template_name_from_path(path):
    return path.replace(asettings.TEMPLATES_NOTIFICATION, '')

def get_data(templateid, data):
    parent, extends = None, None
    if templateid:
        if isinstance(templateid, int):
            template=NewsLetterTemplate.objects.filter(pk=templateid).first()
        else:
            template=templateid
        if template:
            if 'async_notifications' in template.file_path:
                parent = "async_notifications/%s.html"%(template.name)
            else:
                parent = get_template_name_from_path(template.file_path)
    if parent:
        extends = '{% extends "'+parent+'" %}\n\n'
    return (data, extends)



def get_form_data(obj):
    dev = QueryDict()
    if obj.recipient:
        dev = QueryDict(obj.recipient)
    return dev

def extract_template(obj,klass):
    form = klass.get_form(get_form_data(obj))
    klass.set_form(form)
    klass.get_queryset()
    return klass.get_emails_instance()

def get_subject_content(newsletter, context):
    message = Template(newsletter.subject)
    c = Context(context)
    dev = message.render(c)
    return dev

def get_newsletter_content(newsletter):
    inst = get_basemodel_info(newsletter.template.model_base)
    klass = inst[2]()
    emailsiter = extract_template(newsletter, klass)
    data, extends = get_data(newsletter.template, newsletter.message)

    for inst, email in emailsiter:
        context = {
            'email':email,
            klass.name: inst
        }
        template = render_template_newsletter(data, extends, context)
        subject = get_subject_content(newsletter, context)

        yield email, template, subject

def get_connections_config():
    configs = asettings.NEWSLETTER_SEVER_CONFIGS or {}
    return configs

def get_from_email():
    configs = asettings.NEWSLETTER_SEVER_CONFIGS or {}
    if 'from' in configs:
        return configs['from']
    return settings.DEFAULT_FROM_EMAIL

def send_newsletter(newsletter):
    logs = {'exceptions': [], 'success': []}
    messages = []
    with mail.get_connection(**get_connections_config()) as connection:
        if SMTP_DEBUG:
            connection.connection.set_debuglevel(1)
        for email, messagetxt, subject in get_newsletter_content(newsletter):
            message = mail.EmailMessage(subject, messagetxt,
                                        get_from_email(),
                                        [email],
                                        connection=connection
                                        )
            message.content_subtype = "html"
            if newsletter.file:
                if os.path.isfile(settings.MEDIA_ROOT + newsletter.file.name):
                    message.attach_file(settings.MEDIA_ROOT + newsletter.file.name)
            messages.append(message)
        logs['total_sent'] = connection.send_messages(messages)
    return logs

def task_send_newsletter_fnc(pk):
    newsletter = NewsLetter.objects.filter(pk=pk).first()
    logs={'total_sent': 0}
    if newsletter:
        logs = send_newsletter(newsletter)
    return logs['total_sent']

def send_newsletter_task(pk):
    task = NewsLetterTask.object.filter(pk=pk).first()
    if task:
        newsletter = task.template
        send_newsletter(newsletter)