from django.db import models
from django.utils import timezone


class GiftCardInformation(models.Model):
    """Holds the information related to a gift card"""

    redeemable_code = models.CharField(max_length=50, unique=True)
    denomination = models.PositiveIntegerField()
    pin = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    date_of_purchase = models.DateField(default=timezone.now)
    date_created = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    used_on = models.DateTimeField(null=True)
    used_by = models.CharField(max_length=100, blank=True)

    @property
    def date_of_expiry(self):
        """."""

        return self.date_created + timezone.timedelta(days=364)

    def __str__(self):
        """."""

        return self.redeemable_code
