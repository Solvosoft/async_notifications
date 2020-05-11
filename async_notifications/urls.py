from django.urls import path

from async_notifications.views import updatenewscontext, fromnewscontext

urlpatterns = [
    path('context/<int:pk>', updatenewscontext, name="updatenewscontext"),
    path('context/<int:pk>/form', fromnewscontext)
]