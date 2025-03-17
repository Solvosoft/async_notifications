from djgentelella.objectmanagement import BaseObjectManagement

from async_notifications import filterset
from async_notifications.models import EmailTemplate, NewsLetterTask, NewsLetter
from async_notifications import serializers


class NewsLetterTemplateManagement(BaseObjectManagement):
    serializer_class = {
        "list": serializers.NewsLetterTemplateTableSerializer,
        "create": serializers.NewsLetterTemplateSerializer,
        "update": serializers.NewsLetterTemplateSerializer,
        "retrieve": serializers.NewsLetterTemplateSerializer,
        "get_values_for_update": serializers.NewsLetterTemplateSerializer,
    }
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication, SessionAuthentication)
    queryset = EmailTemplate.objects.all()

    search_fields = ["subject"]  # for the global search
    filterset_class = filterset.NewsLetterTemplateFilterSet
    ordering_fields = ["pk", "title"]
    ordering = ("-pk",)  # default order
    operation_type = ""


class NewsLetterManagement(BaseObjectManagement):
    serializer_class = {
        "list": serializers.NewsLetterTableSerializer,
        "create": serializers.NewsLetterSerializer,
        "update": serializers.NewsLetterSerializer,
        "retrieve": serializers.NewsLetterSerializer,
        "get_values_for_update": serializers.NewsLetterSerializer,
    }
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication, SessionAuthentication)
    queryset = NewsLetter.objects.all()

    search_fields = ["subject"]  # for the global search
    filterset_class = filterset.NewsLetterTemplateFilterSet
    ordering_fields = ["pk", "template"]
    ordering = ("-pk",)  # default order
    operation_type = ""


class NewsLetterTaskManagement(BaseObjectManagement):
    serializer_class = {
        "list": serializers.NewsLetterTaskTableSerializer,
        "create": serializers.NewsLetterTaskSerializer,
        "update": serializers.NewsLetterTaskSerializer,
        "retrieve": serializers.NewsLetterTaskSerializer,
        "get_values_for_update": serializers.NewsLetterTaskSerializer,
    }
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication, SessionAuthentication)
    queryset = NewsLetterTask.objects.all()

    search_fields = ["template", "task_id"]  # for the global search
    filterset_class = filterset.NewsLetterTaskFilterSet
    ordering_fields = ["pk", "send_date"]
    ordering = ("-pk",)  # default order
    operation_type = ""
