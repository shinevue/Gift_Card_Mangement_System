from django.db.models import Count
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView, UpdateView, RedirectView

from dispenser.forms import GiftCardDetailForm
from core.models import GiftCardInformation


class DenominationSelectView(TemplateView):
    """."""

    template_name = "dispenser/denominationselect.html"
    extra_context = {
        "denominations": GiftCardInformation.objects.filter(is_used=False)
        .values("denomination")
        .annotate(denomination_count=Count("denomination"))
    }


class GiftCardDetailRedirectView(RedirectView):
    """."""

    pattern_name = "gc-detail-update"
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        """."""

        denomination = kwargs.get("denomination")

        gc_to_display = (
            GiftCardInformation.objects.filter(is_used=False, denomination=denomination)
            .order_by("date_of_purchase")
            .first()
        )
        return super(GiftCardDetailRedirectView, self).get_redirect_url(
            *args, pk=gc_to_display.id
        )


class GiftCardUpdateView(UpdateView):
    """."""

    form_class = GiftCardDetailForm
    model = GiftCardInformation
    template_name = "dispenser/giftcarddetail.html"
    success_url = reverse_lazy("index")

    def post(self, request, *args, **kwargs):
        """."""

        gc_instance = self.get_object()
        gc_instance.used_on = timezone.now()
        gc_instance.is_used = True
        gc_instance.save()
        return super().post(request, *args, **kwargs)
