from django.urls import path

from .views import index

# app_name = "demoapp"
urlpatterns = [
    path("", index, name="home"),
]
