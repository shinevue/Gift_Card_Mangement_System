from dataclasses import asdict
from datetime import datetime

import falcon

from gcmanager.domain import GiftCard
from tests.factories import GiftCardFactory
from tests.integration.db_app_test_case import MongoDBAndAppAwareTestCase


class TestGiftCardAssetInformationAPI(MongoDBAndAppAwareTestCase):
    def setUp(self) -> None:
        super(TestGiftCardAssetInformationAPI, self).setUp()
        self.api_path = "/api/giftcards/assets/"

    @staticmethod
    def _prepare_to_be_inserted_gift_cards(gift_cards: list[GiftCard]) -> list[dict]:
        serialized_gift_cards = []
        for gift_card in gift_cards:
            serialized_gift_card = asdict(gift_card)
            date_of_issue = serialized_gift_card.pop("date_of_issue")
            serialized_gift_card["date_of_issue"] = datetime(
                year=date_of_issue.year,
                month=date_of_issue.month,
                day=date_of_issue.day,
                hour=0,
                minute=0,
                second=0,
                microsecond=0,
            )
            identity = serialized_gift_card.pop("id")
            serialized_gift_card.update({"_id": identity})
            serialized_gift_cards.append(serialized_gift_card)
        return serialized_gift_cards

    def test_returns_zero_for_all_when_db_empty(self) -> None:
        response = self.simulate_get(self.api_path)
        expected_response = {
            "status": "ok",
            "data": {"total": 0, "used": 0, "unused": 0},
        }
        self.assertEqual(falcon.HTTP_OK, response.status)
        self.assertEqual(expected_response, response.json)

    def test_returns_expected_data_when_no_gift_card_is_used(self) -> None:
        gift_cards = GiftCardFactory.build_batch(10, denomination=500)
        serialized_gift_cards = self._prepare_to_be_inserted_gift_cards(gift_cards)
        self.collection.insert_many(serialized_gift_cards)
        response = self.simulate_get(self.api_path)
        expected_response = {
            "status": "ok",
            "data": {"total": 5000, "used": 0, "unused": 5000},
        }
        self.assertEqual(falcon.HTTP_OK, response.status)
        self.assertEqual(expected_response, response.json)

    def test_returns_expected_data_when_some_gift_cards_are_used(self) -> None:
        used_gift_cards = GiftCardFactory.build_batch(
            5,
            is_used=True,
            denomination=1000,
        )
        unused_gift_cards = GiftCardFactory.build_batch(5, denomination=1000)
        serialized_gift_cards = self._prepare_to_be_inserted_gift_cards(
            used_gift_cards + unused_gift_cards,
        )
        self.collection.insert_many(serialized_gift_cards)
        response = self.simulate_get(self.api_path)
        expected_response = {
            "status": "ok",
            "data": {"total": 10000, "used": 5000, "unused": 5000},
        }
        self.assertEqual(falcon.HTTP_OK, response.status)
        self.assertEqual(expected_response, response.json)
