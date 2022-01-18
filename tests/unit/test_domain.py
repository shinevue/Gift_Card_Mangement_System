import datetime
from unittest import TestCase

from gcmanager.domain import Denomination
from gcmanager.domain import GiftCardAssetSummary
from gcmanager.domain import Money
from tests.unit.factories import GiftCardFactory


class TestGiftCard(TestCase):
    def test_returns_expected_date_of_expiry(self) -> None:
        gift_card = GiftCardFactory(
            date_of_issue=datetime.date(year=2022, month=1, day=3),
        )
        expected_expiry_date = datetime.date(year=2023, month=1, day=3)
        self.assertEqual(expected_expiry_date, gift_card.date_of_expiry)


class TestGiftCardAssetSummary(TestCase):
    def test_returns_expected_unused_amount(self) -> None:
        gift_card_asset_summary = GiftCardAssetSummary(
            total=Money(1200),
            used=Money(400),
        )
        self.assertEqual(Denomination(800), gift_card_asset_summary.unused)
