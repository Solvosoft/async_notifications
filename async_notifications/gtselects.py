from django.contrib.auth.models import User
from djgentelella.groute import register_lookups
from djgentelella.views.select2autocomplete import BaseSelect2View


@register_lookups(prefix="contact", basename="contact")
class ContactLookup(BaseSelect2View):
    model = User
    fields = ["email"]
