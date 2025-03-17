from django_filters import (
    DateFromToRangeFilter,
    FilterSet,
    filterset,
    DateTimeFromToRangeFilter,
)
from djgentelella.fields.drfdatetime import DateRangeTextWidget, DateTimeRangeTextWidget

from async_notifications.models import (
    EmailNotification,
    EmailTemplate,
    NewsLetterTemplate,
    NewsLetter,
    NewsLetterTask,
)


class EmailNotificationFilterSet(FilterSet):
    create_datetime = DateTimeFromToRangeFilter(
        widget=DateTimeRangeTextWidget(attrs={"placeholder": "YYYY/MM/DD"})
    )

    class Meta:
        model = EmailNotification
        fields = {
            "subject": ["icontains"],
            "message": ["icontains"],
            "recipient": ["icontains"],
            "enqueued": ["exact"],
            "sent": ["exact"],
            "problems": ["exact"],
        }


class EmailTemplateFilterSet(FilterSet):
    class Meta:
        model = EmailTemplate
        fields = {
            "code": ["icontains"],
            "subject": ["icontains"],
            "message": ["icontains"],
        }


class NewsLetterTemplateFilterSet(FilterSet):
    class Meta:
        model = NewsLetterTemplate
        fields = {
            "title": ["icontains"],
            "name": ["icontains"],
            "message": ["icontains"],
            "model_base": ["icontains"],
        }


class NewsLetterFilterSet(FilterSet):
    create_datetime = DateFromToRangeFilter(
        widget=DateRangeTextWidget(attrs={"placeholder": "YYYY/MM/DD"})
    )

    class Meta:
        model = NewsLetter
        fields = {
            "subject": ["icontains"],
            "message": ["icontains"],
            "filters": ["icontains"],
        }


class NewsLetterTaskFilterSet(FilterSet):
    send_date = DateFromToRangeFilter(
        widget=DateRangeTextWidget(attrs={"placeholder": "YYYY/MM/DD"})
    )
    template = filterset.CharFilter(source="template__name")

    class Meta:
        model = NewsLetterTask
        fields = {
            "task_id": ["icontains"],
        }
