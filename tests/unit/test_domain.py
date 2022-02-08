import datetime
import json
from unittest import TestCase

from gcmanager.domain import Denomination
from gcmanager.domain import GiftCardAssetSummary
from gcmanager.domain import Money
from gcmanager.domain import SuccessfulResponse
from tests.factories import GiftCardFactory


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


class TestSuccessfulResponse(TestCase):
    def setUp(self) -> None:
        self.serialized_dict_data = {
            "used": 800,
            "total": 1000,
            "unused": 200,
        }
        self.serialized_list_data = [
            {"field": "value"},
            {"field": "value"},
            {"field": "value"},
        ]
        self.successful_dict_response = SuccessfulResponse(self.serialized_dict_data)
        self.successful_list_response = SuccessfulResponse(self.serialized_list_data)

    def test_serializes_to_expected_data_dict(self) -> None:
        expected_data = json.dumps(
            {
                "status": "ok",
                "data": self.serialized_dict_data,
            },
        )
        self.assertEqual(expected_data, self.successful_dict_response.serialize())

    def test_serializes_to_expected_data_list(self) -> None:
        expected_data = json.dumps(
            {
                "status": "ok",
                "data": self.serialized_list_data,
            },
        )
        self.assertEqual(expected_data, self.successful_list_response.serialize())
