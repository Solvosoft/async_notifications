from django.urls import path

from async_notifications.views import updatenewscontext, fromnewscontext, preview_email_newsletters

urlpatterns = [
    path('context/<int:pk>', updatenewscontext, name="updatenewscontext"),
    path('context/<int:pk>/form', fromnewscontext),
    path('context/<int:pk>/preview', preview_email_newsletters, name='preview_newsletter_emails')
]