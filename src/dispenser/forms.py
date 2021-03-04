from django.forms import ModelForm, fields

from core.models import GiftCardInformation


class GiftCardDetailForm(ModelForm):
    """."""

    redeemable_code = fields.CharField(max_length=50, disabled=True)
    denomination = fields.IntegerField(disabled=True)
    pin = fields.CharField(max_length=100, disabled=True)
    source = fields.CharField(max_length=100, disabled=True)
    date_of_purchase = fields.DateField(disabled=True)
    used_by = fields.CharField(max_length=100, required=True)
    # date_created = fields.DateTimeField(disabled=True)

    class Meta:
        model = GiftCardInformation
        fields = (
            "redeemable_code",
            "denomination",
            "pin",
            "source",
            "date_of_purchase",
            # "date_created",
            "used_by",
        )
