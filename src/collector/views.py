from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin

from collector.forms import GiftCardCollectorForm


class GiftCardCollectorView(SuccessMessageMixin, CreateView):
    """."""

    form_class = GiftCardCollectorForm
    template_name = "collector/gccollector.html"
    success_message = "Code %(redeemable_code)s has been added"
    success_url = reverse_lazy("gc-collector")
