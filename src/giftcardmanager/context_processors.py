from django.db.models import Sum
from django.db.models.functions import Coalesce

from core.models import GiftCardInformation


def asset_information(request):
    """."""

    field_name = "sum_of_denomination"
    aggregation_dict = {field_name: Coalesce(Sum("denomination"), 0)}
    gcs = GiftCardInformation.objects.all()

    return {
        "unused_asset": gcs.filter(is_used=False)
        .aggregate(**aggregation_dict)
        .get(field_name),
        "used_asset": gcs.filter(is_used=True)
        .aggregate(**aggregation_dict)
        .get(field_name),
        "total_asset": gcs.aggregate(**aggregation_dict).get(field_name),
    }
