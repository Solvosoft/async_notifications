from djgentelella.fields.files import ChunkedFileField
from rest_framework import serializers

from async_notifications.models import (
    EmailNotification,
    EmailTemplate,
    NewsLetterTemplate,
    NewsLetter,
    NewsLetterTask,
)


class EmailNotificationSerializer(serializers.ModelSerializer):
    actions = serializers.SerializerMethodField()
    file = ChunkedFileField()

    def get_actions(self, obj):
        return {"destroy": True, "update": True, "detail": True, "sendemail": True}

    class Meta:
        model = EmailNotification
        fields = "__all__"


class EmailNotificationSendEmail(serializers.Serializer):
    items = serializers.PrimaryKeyRelatedField(
        many=True, queryset=EmailNotification.objects.all()
    )


class EmailNotificationTableSerializer(serializers.Serializer):
    data = serializers.ListField(child=EmailNotificationSerializer(), required=True)
    draw = serializers.IntegerField(required=True)
    recordsFiltered = serializers.IntegerField(required=True)
    recordsTotal = serializers.IntegerField(required=True)


class EmailTemplateSerializer(serializers.ModelSerializer):
    actions = serializers.SerializerMethodField()

    def get_actions(self, obj):
        return {"destroy": True, "update": True, "detail": True}

    class Meta:
        model = EmailTemplate
        fields = "__all__"


class EmailTemplateTableSerializer(serializers.Serializer):
    data = serializers.ListField(child=EmailTemplateSerializer(), required=True)
    draw = serializers.IntegerField(required=True)
    recordsFiltered = serializers.IntegerField(required=True)
    recordsTotal = serializers.IntegerField(required=True)


class NewsLetterTemplateSerializer(serializers.ModelSerializer):
    actions = serializers.SerializerMethodField()

    def get_actions(self, obj):
        return {"destroy": True, "update": True, "detail": True}

    class Meta:
        model = NewsLetterTemplate
        fields = "__all__"


class NewsLetterTemplateTableSerializer(serializers.Serializer):
    data = serializers.ListField(child=NewsLetterTemplateSerializer(), required=True)
    draw = serializers.IntegerField(required=True)
    recordsFiltered = serializers.IntegerField(required=True)
    recordsTotal = serializers.IntegerField(required=True)


class NewsLetterSerializer(serializers.ModelSerializer):
    actions = serializers.SerializerMethodField()

    def get_actions(self, obj):
        return {"destroy": True, "update": True, "detail": True}

    class Meta:
        model = NewsLetter
        fields = "__all__"


class NewsLetterTableSerializer(serializers.Serializer):
    data = serializers.ListField(child=NewsLetterSerializer(), required=True)
    draw = serializers.IntegerField(required=True)
    recordsFiltered = serializers.IntegerField(required=True)
    recordsTotal = serializers.IntegerField(required=True)


class NewsLetterTaskSerializer(serializers.ModelSerializer):
    actions = serializers.SerializerMethodField()

    def get_actions(self, obj):
        return {"destroy": True, "update": True, "detail": True}

    class Meta:
        model = NewsLetterTask
        fields = "__all__"


class NewsLetterTaskTableSerializer(serializers.Serializer):
    data = serializers.ListField(child=NewsLetterTaskSerializer(), required=True)
    draw = serializers.IntegerField(required=True)
    recordsFiltered = serializers.IntegerField(required=True)
    recordsTotal = serializers.IntegerField(required=True)
