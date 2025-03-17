from django.urls import path, include
from rest_framework.routers import DefaultRouter

from views import email_to_tagify
from .viewsets import emailnotification, newsletter as newsletterviewset
from .views import (
    email_notification_view,
    email_template,
    newsletter,
    newsletter_template,
    newsletter_tasks,
)

router = DefaultRouter()

router.register(
    prefix="emailnotification",
    viewset=emailnotification.EmailNotificationManagement,
    basename="api-emailnotification",
)
router.register(
    prefix="emailtemplate",
    viewset=emailnotification.EmailTemplateManagement,
    basename="api-emailtemplate",
)
router.register(
    prefix="newslettertemplate",
    viewset=newsletterviewset.NewsLetterTemplateManagement,
    basename="api-newslettertemplate",
)

router.register(
    prefix="newsletter",
    viewset=newsletterviewset.NewsLetterManagement,
    basename="api-newsletter",
)
router.register(
    prefix="newslettertask",
    viewset=newsletterviewset.NewsLetterTaskManagement,
    basename="api-newslettertask",
)

app_name = "async_notifications"

urlpatterns = [
    path("objapi/", include(router.urls)),
    path("email_notification/", email_notification_view, name="email_notification"),
    path("email_template/", email_template, name="email_template"),
    path("newsletter/", newsletter),
    path("newsletter_template/", newsletter_template),
    path("newsletter_tasks/", newsletter_tasks),
    path("email_to_tagify/", email_to_tagify, name="email_to_tagify"),
]
