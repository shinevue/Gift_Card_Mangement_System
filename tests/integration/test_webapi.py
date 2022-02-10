import datetime

import falcon

from tests.factories import GiftCardFactory
from tests.integration.db_app_test_case import MongoDBAndAppAwareTestCase
from tests.integration.utils import prepare_to_be_inserted_gift_card


class TestGiftCardAssetInformationAPI(MongoDBAndAppAwareTestCase):
    def setUp(self) -> None:
        super(TestGiftCardAssetInformationAPI, self).setUp()
        self.api_path = "/api/giftcards/assets/"

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
        serialized_gift_cards = [
            prepare_to_be_inserted_gift_card(gift_card) for gift_card in gift_cards
        ]
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
        serialized_gift_cards = [
            prepare_to_be_inserted_gift_card(gift_card)
            for gift_card in used_gift_cards + unused_gift_cards
        ]
        self.collection.insert_many(serialized_gift_cards)
        response = self.simulate_get(self.api_path)
        expected_response = {
            "status": "ok",
            "data": {"total": 10000, "used": 5000, "unused": 5000},
        }
        self.assertEqual(falcon.HTTP_OK, response.status)
        self.assertEqual(expected_response, response.json)


class TestMarkGiftCardUsedAPI(MongoDBAndAppAwareTestCase):
    def test_returns_200_when_gift_card_successfully_mark_used(self) -> None:
        gift_card = GiftCardFactory()
        serialized_gift_card = prepare_to_be_inserted_gift_card(gift_card)
        self.collection.insert_one(serialized_gift_card)
        response = self.simulate_post(f"/api/giftcards/{gift_card.id}/mark-used/")
        gift_card_in_db = self.collection.find_one({"_id": gift_card.id})
        self.assertEqual(falcon.HTTP_200, response.status)
        self.assertTrue(gift_card_in_db["is_used"])

    def test_returns_400_when_gift_card_not_found(self) -> None:
        gift_card = GiftCardFactory()
        response = self.simulate_post(f"/api/giftcards/{gift_card.id}/mark-used/")
        self.assertEqual(falcon.HTTP_400, response.status)

    def test_returns_400_when_gift_card_already_used(self) -> None:
        gift_card = GiftCardFactory(is_used=True)
        serialized_gift_card = prepare_to_be_inserted_gift_card(gift_card)
        self.collection.insert_one(serialized_gift_card)
        response = self.simulate_post(f"/api/giftcards/{gift_card.id}/mark-used/")
        self.assertEqual(falcon.HTTP_400, response.status)

    def test_returns_404_when_gift_card_id_invalid(self) -> None:
        gift_card = GiftCardFactory(id="123kjasdjlk")
        response = self.simulate_post(f"/api/giftcards/{gift_card.id}/mark-used/")
        self.assertEqual(falcon.HTTP_404, response.status)


class TestDenominationAPI(MongoDBAndAppAwareTestCase):
    def setUp(self) -> None:
        super(TestDenominationAPI, self).setUp()
        self.api_path = "/api/giftcards/denominations/"

    def test_returns_empty_list_when_db_empty(self) -> None:
        response = self.simulate_get(self.api_path)
        self.assertEqual({"status": "ok", "data": []}, response.json)
        self.assertEqual(falcon.HTTP_200, response.status)

    def test_returns_empty_list_when_db_has_gcs(self) -> None:
        gift_cards = [
            GiftCardFactory(is_used=False, denomination=100),
            GiftCardFactory(is_used=False, denomination=200),
            GiftCardFactory(is_used=False, denomination=300),
            GiftCardFactory(is_used=False, denomination=400),
            GiftCardFactory(is_used=False, denomination=500),
            GiftCardFactory(is_used=False, denomination=1000),
            GiftCardFactory(is_used=True, denomination=200),
            GiftCardFactory(is_used=True, denomination=2000),
            GiftCardFactory(is_used=True, denomination=2000),
            GiftCardFactory(is_used=True, denomination=2000),
            GiftCardFactory(is_used=True, denomination=2000),
            GiftCardFactory(is_used=True, denomination=2000),
            GiftCardFactory(is_used=True, denomination=2000),
        ]
        serialized_gift_cards = [
            prepare_to_be_inserted_gift_card(gift_card) for gift_card in gift_cards
        ]
        expected_denominations = [100, 200, 300, 400, 500, 1000]
        self.collection.insert_many(serialized_gift_cards)
        response = self.simulate_get(self.api_path)
        self.assertEqual(
            {"status": "ok", "data": expected_denominations},
            response.json,
        )
        self.assertEqual(falcon.HTTP_200, response.status)

    def test_returns_empty_list_when_all_gift_cards_used(self) -> None:
        response = self.simulate_get(self.api_path)
        gift_cards = GiftCardFactory.build_batch(10, is_used=True)
        serialized_gift_cards = [
            prepare_to_be_inserted_gift_card(gift_card) for gift_card in gift_cards
        ]
        self.collection.insert_many(serialized_gift_cards)
        self.assertEqual({"status": "ok", "data": []}, response.json)
        self.assertEqual(falcon.HTTP_200, response.status)


class TestNearExpiryGiftCardAPI(MongoDBAndAppAwareTestCase):
    def test_returns_404_when_denomination_invalid(self) -> None:
        response = self.simulate_get("/api/giftcards/denominations/abcd/")
        self.assertEqual(falcon.HTTP_404, response.status)

    def test_returns_200_when_gift_card_found(self) -> None:
        gift_cards = [
            GiftCardFactory(
                date_of_issue=datetime.date.today().replace(month=month),
                denomination=200,
                timestamp=datetime.datetime.now().replace(microsecond=0),
            )
            for month in range(1, 13)
        ]
        serialized_gift_cards = [
            prepare_to_be_inserted_gift_card(gc) for gc in gift_cards
        ]
        self.collection.insert_many(serialized_gift_cards)
        response = self.simulate_get("/api/giftcards/denominations/200/")
        self.assertEqual(falcon.HTTP_200, response.status)
        expected_gift_card = gift_cards[0]
        expected_response = {
            "status": "ok",
            "data": {
                "id": str(expected_gift_card.id),
                "redeem_code": expected_gift_card.redeem_code,
                "date_of_issue": expected_gift_card.date_of_issue.isoformat(),
                "pin": expected_gift_card.pin,
                "source": expected_gift_card.source,
                "denomination": expected_gift_card.denomination,
                "timestamp": expected_gift_card.timestamp.isoformat(),
                "date_of_expiry": expected_gift_card.date_of_expiry.isoformat(),
                "is_used": expected_gift_card.is_used,
            },
        }
        self.assertEqual(expected_response, response.json)

    def test_returns_404_when_gift_card_invalid(self) -> None:
        gift_cards = [
            GiftCardFactory(
                date_of_issue=datetime.date.today().replace(month=month),
                denomination=200,
                timestamp=datetime.datetime.now().replace(microsecond=0),
                is_used=True,
            )
            for month in range(1, 13)
        ]
        serialized_gift_cards = [
            prepare_to_be_inserted_gift_card(gc) for gc in gift_cards
        ]
        self.collection.insert_many(serialized_gift_cards)
        response = self.simulate_get("/api/giftcards/denominations/200/")
        self.assertEqual(falcon.HTTP_404, response.status)
