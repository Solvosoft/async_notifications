from django.http import JsonResponse
from django.shortcuts import render

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

def fromnewscontext(request, pk):
    dev = ""
    obj = NewsLetterTemplate.objects.filter(pk=pk).first()
    if obj:
        inst = get_basemodel_info(obj.model_base)
        if inst:
            klass = inst[2]()
            dev = str(klass.get_form())
    return JsonResponse({'form': dev })