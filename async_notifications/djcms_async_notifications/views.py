from django.shortcuts import render

# Create your views here.
from .forms import NotificationForm
from django.http.response import HttpResponse, Http404
from django.utils.translation import ugettext_lazy as _
from async_notifications.utils import send_email_from_template, extract_emails
from async_notifications.djcms_async_notifications.utils import get_str_base64url

from django.contrib.contenttypes.models import ContentType
from async_notifications.register import update_template_context
from async_notifications.models import EmailTemplate

update_template_context('page_email', 'Send page by email',
                        [('url', str(_('Article url'))),
                         ('page', str(
                             _('Article object [title, lead_in, \
                             content, author, owner, publishing_date, \
                             is_published, is_featured ]'))),
                         ('extra_message', str(_('User extra message'))),
                         ('user', str(_('Sender user')))]
                        )


def extract_context(form):
    uri = get_str_base64url(form.cleaned_data['uri'])

    app_label, model = form.cleaned_data['name'].split(".")
    page_type = ContentType.objects.get(app_label=app_label,
                                        model=model)
    page = page_type.get_object_for_this_type(pk=form.cleaned_data['pk'])

    return {'page': page, 'url': uri}


def get_email_modal(request):

    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            context = extract_context(form)
            context['extra_message'] = form.cleaned_data['extra_message']
            send_email_from_template(
                form.cleaned_data['template'].code,  # code
                extract_emails(form.cleaned_data['recipient']),
                enqueued=False,
                user=request.user,
                context=context
            )

            # #div_success is important because is how i comunicate with iframe
            return HttpResponse(
                _("""<div id="div_success">Email sent successfully</div>"""))
    else:
        uri = request.GET.get('uri', '')
        pk = request.GET.get('pk', '')
        name = request.GET.get('name', '')

        if not all([uri, pk, name]):
            raise Http404()
        initial = {'uri': uri, 'pk': pk, 'name': name}
        try:
            initial['template'] = EmailTemplate.objects.get(code='page_email')
        except:
            pass
        form = NotificationForm(initial=initial)

    response = render(request, 'djcms_async_notifications/page_form_email.html',
                      {
                          'form': form,
                      }
                      )
    # response.render()

    return response
