from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from async_notifications import serializers
from async_notifications import filterset
from djgentelella.objectmanagement import BaseObjectManagement
from async_notifications.models import EmailNotification, EmailTemplate
from ..tasks import send_email


class EmailNotificationManagement(BaseObjectManagement):
    serializer_class = {
        "list": serializers.EmailNotificationTableSerializer,
        "create": serializers.EmailNotificationSerializer,
        "update": serializers.EmailNotificationSerializer,
        "retrieve": serializers.EmailNotificationSerializer,
        "get_values_for_update": serializers.EmailNotificationSerializer,
        "send_email": serializers.EmailNotificationSendEmail,
    }
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication, SessionAuthentication)
    queryset = EmailNotification.objects.all()

    search_fields = ["subject"]  # for the global search
    filterset_class = filterset.EmailNotificationFilterSet
    ordering_fields = ["pk", "create_datetime", "enqueued", "sent", "problems"]
    ordering = ("-pk",)  # default order
    operation_type = ""

    @action(methods=["post"], detail=True)
    def send_email(self, request, pk):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            for email in serializer.validated_data["items"]:
                send_email.delay(email.pk)
        return Response({"result": True}, status=status.HTTP_200_OK)


class EmailTemplateManagement(BaseObjectManagement):
    serializer_class = {
        "list": serializers.EmailTemplateTableSerializer,
        "create": serializers.EmailTemplateSerializer,
        "update": serializers.EmailTemplateSerializer,
        "retrieve": serializers.EmailTemplateSerializer,
        "get_values_for_update": serializers.EmailTemplateSerializer,
    }
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication, SessionAuthentication)
    queryset = EmailTemplate.objects.all()

    search_fields = ["subject"]  # for the global search
    filterset_class = filterset.EmailTemplateFilterSet
    ordering_fields = ["pk", "code"]
    ordering = ("-pk",)  # default order
    operation_type = ""
