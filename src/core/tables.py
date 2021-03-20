from django_tables2 import tables

from core.models import GiftCardInformation


class AllGiftCardsTable(tables.Table):
    """."""

    class Meta:
        model = GiftCardInformation
        row_attrs = {"data-id": lambda record: record.pk}
        empty_text = "Oops! No gift cards found!"
        order_by = "-date_of_purchase"
        exclude = ("id",)
