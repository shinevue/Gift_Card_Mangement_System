from django.views.generic import TemplateView
from django_tables2 import SingleTableView

from core.tables import AllGiftCardsTable
from core.models import GiftCardInformation


class IndexView(TemplateView):
    """."""

    template_name = "core/index.html"


class AllGiftCardsTableView(SingleTableView):
    """."""

    template_name = "core/allgcs.html"
    table_class = AllGiftCardsTable
    queryset = GiftCardInformation.objects.all()
