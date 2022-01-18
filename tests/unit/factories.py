from datetime import date
from datetime import datetime

from factory import Factory
from factory.fuzzy import FuzzyChoice
from factory.fuzzy import FuzzyDate
from factory.fuzzy import FuzzyInteger
from factory.fuzzy import FuzzyNaiveDateTime
from factory.fuzzy import FuzzyText

from gcmanager.domain import GiftCard
from gcmanager.domain import GiftCardAssetSummary
from gcmanager.domain import GiftCardUpdateRequest


class GiftCardAssetSummaryFactory(Factory):
    class Meta:
        model = GiftCardAssetSummary

    total = FuzzyInteger(8_000, 15_000)
    used = FuzzyInteger(400, 7_000)


class GiftCardFactory(Factory):
    class Meta:
        model = GiftCard

    id = FuzzyText(length=16)
    redeem_code = FuzzyText(length=14)
    date_of_issue = FuzzyDate(start_date=date.today())
    pin = FuzzyInteger(low=1_000_000_000_000_000, high=9_999_999_999_999_999)
    timestamp = FuzzyNaiveDateTime(start_dt=datetime.now())
    is_used = False
    source = FuzzyChoice(["AMAZON", "WOOHOO", "MAGICPIN", "HDFC SMARTBUY"])
    denomination = FuzzyChoice([50, 100, 200, 500, 1_000, 2_000, 10_000])


class GiftCardUpdateRequestFactory(Factory):
    class Meta:
        model = GiftCardUpdateRequest

    id = FuzzyText(length=16)
    redeem_code = FuzzyText(length=14)
    date_of_issue = FuzzyDate(start_date=date.today())
    pin = FuzzyInteger(low=1_000_000_000_000_000, high=9_999_999_999_999_999)
    source = FuzzyChoice(["AMAZON", "WOOHOO", "MAGICPIN", "HDFC SMARTBUY"])
    denomination = FuzzyChoice([50, 100, 200, 500, 1_000, 2_000, 10_000])
