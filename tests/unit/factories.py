from factory import Factory
from factory.fuzzy import FuzzyInteger

from gcmanager.domain import GiftCardAssetSummary


class GiftCardAssetSummaryFactory(Factory):
    class Meta:
        model = GiftCardAssetSummary

    total = FuzzyInteger(8_000, 15_000)
    used = FuzzyInteger(400, 7_000)
