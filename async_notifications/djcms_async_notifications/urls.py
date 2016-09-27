
from django.conf.urls import url
from .views import get_email_modal

urlpatterns = [
    url(r'^get_email_modal$',  get_email_modal, name="get_email_modal"),

]
