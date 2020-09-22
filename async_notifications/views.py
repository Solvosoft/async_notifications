from django.http import JsonResponse
from django.shortcuts import render
from django.http.request import QueryDict
# Create your views here.
from async_notifications.models import NewsLetterTemplate
from async_notifications.utils import get_newsletter_context, get_basemodel_info


def updatenewscontext(request, pk):
    dev = []
    obj = NewsLetterTemplate.objects.filter(pk=pk).first()
    if obj:
        for i in get_newsletter_context(obj.model_base):
            dev.append(
                {
                    'id': i[0],
                    'text': i[0]+ " -- "+i[1]
                }
            )

    return JsonResponse({'results': dev, "pagination": {"more": False}})


def get_form_data(request):
    dev = None
    try:
        dev = QueryDict(request.POST.get('recipient'))
    except:
        dev = None

    return dev

def fromnewscontext(request, pk):
    dev = ""
    media = ""
    obj = NewsLetterTemplate.objects.filter(pk=pk).first()
    if obj:
        inst = get_basemodel_info(obj.model_base)
        if inst:
            klass = inst[2]()
            f = klass.get_form(get_form_data(request))
            dev = str(f)
            media = str(f.media)
    return JsonResponse({'form': dev, 'media': media })


def preview_email_newsletters(request, pk):
    dev = []
    obj = NewsLetterTemplate.objects.filter(pk=pk).first()
    if obj:
        inst = get_basemodel_info(obj.model_base)
        if inst:
            klass = inst[2]()
            form = klass.get_form(get_form_data(request))
            klass.set_form(form)
            klass.get_queryset()
            dev = klass.get_emails()
    return JsonResponse({'emails': dev })