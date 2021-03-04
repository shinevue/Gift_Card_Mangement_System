from django import forms

from core.models import GiftCardInformation
from collector.widgets import DatePickerFieldWidget


class GiftCardCollectorForm(forms.ModelForm):
    """Form to collect gift card information"""

    class Meta:
        """."""

        model = GiftCardInformation
        fields = (
            "redeemable_code",
            "denomination",
            "pin",
            "source",
            "date_of_purchase",
        )
        widgets = {
            "date_of_purchase": DatePickerFieldWidget,
        }
