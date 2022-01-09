import datetime
from unittest import TestCase

from gcmanager.domain import Denomination
from gcmanager.domain import GiftCard
from gcmanager.domain import GiftCardAssetSummary
from gcmanager.domain import GiftCardID
from gcmanager.domain import RedeemCode


class TestGiftCard(TestCase):
    def test_returns_expected_date_of_expiry(self) -> None:
        gift_card = GiftCard(
            id=GiftCardID("blah-blah"),
            redeem_code=RedeemCode("1234-XPGJ21-T3UF"),
            date_of_issue=datetime.date(year=2022, month=1, day=3),
            pin=10293910,
            timestamp=datetime.datetime(
                year=2022,
                month=1,
                day=4,
                hour=13,
                minute=10,
                second=0,
            ),
            is_used=False,
            denomination=Denomination(500),
            source="AMAZON",
        )
        expected_expiry_date = datetime.date(year=2023, month=1, day=3)
        self.assertEqual(expected_expiry_date, gift_card.date_of_expiry)


class TestGiftCardAssetSummary(TestCase):
    def test_returns_expected_unused_amount(self) -> None:
        gift_card_asset_summary = GiftCardAssetSummary(
            total=Denomination(1200),
            used=Denomination(400),
        )
        self.assertEqual(Denomination(800), gift_card_asset_summary.unused)
