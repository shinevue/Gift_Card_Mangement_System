from django.db.models import Sum

from core.models import GiftCardInformation


def asset_information(request):
    """."""

    gcs = GiftCardInformation.objects.all()

    return {
        "unused_asset": gcs.filter(is_used=False)
        .aggregate(Sum("denomination"))
        .get("denomination__sum"),
        "used_asset": gcs.filter(is_used=True)
        .aggregate(Sum("denomination"))
        .get("denomination__sum"),
        "total_asset": gcs.aggregate(Sum("denomination")).get("denomination__sum"),
    }
