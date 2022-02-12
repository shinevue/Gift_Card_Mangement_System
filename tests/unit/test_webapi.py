import json
from unittest import TestCase

import falcon
from falcon import errors
from falcon import testing
from mockito import mock
from mockito import when

from gcmanager.domain import Denomination
from gcmanager.domain import GiftCardAssetSummary
from gcmanager.domain import Money
from gcmanager.exceptions import GiftCardAlreadyExists
from gcmanager.exceptions import GiftCardAlreadyUsed
from gcmanager.exceptions import GiftCardNotFound
from gcmanager.exceptions import GiftCardNotFoundForDenomination
from gcmanager.webapi import DenominationResource
from gcmanager.webapi import GiftCardAssetInformationResource
from gcmanager.webapi import GiftCardResource
from gcmanager.webapi import MarkGiftCardUsedResource
from gcmanager.webapi import NearExpiryGiftCardResource
from tests.factories import GiftCardCreateRequestFactory
from tests.factories import GiftCardFactory
from tests.factories import GiftCardPayloadFactory
from tests.factories import GiftCardUpdateRequestFactory


class TestGiftCardAssetInformationResource(TestCase):
    def setUp(self) -> None:
        self.use_case = mock()
        self.resource = GiftCardAssetInformationResource(self.use_case)

    def test_returns_expected_response(self) -> None:
        when(self.use_case).summarize().thenReturn(
            GiftCardAssetSummary(total=Money(1000), used=Money(800)),
        )
        request = testing.create_req()
        response = falcon.Response()
        self.resource.on_get(request, response)
        expected_body = {
            "status": "ok",
            "data": {
                "total": 1000,
                "used": 800,
                "unused": 200,
            },
        }
        self.assertEqual(falcon.HTTP_200, response.status)
        self.assertEqual(expected_body, json.loads(response.text))


class TestGiftCardResource(TestCase):
    def setUp(self) -> None:
        self.create_use_case = mock()
        self.get_unused_gc_use_case = mock()
        self.update_gc_use_case = mock()
        self.resource = GiftCardResource(
            self.create_use_case,
            self.get_unused_gc_use_case,
            self.update_gc_use_case,
        )
        self.gift_cards = GiftCardFactory.build_batch(5, is_used=False)

    def test_returns_expected_response_when_get(self) -> None:
        request = testing.create_req()
        response = falcon.Response()
        when(self.get_unused_gc_use_case).fetch().thenReturn(self.gift_cards)
        self.resource.on_get(request, response)
        expected_body = {
            "status": "ok",
            "data": [
                {
                    "id": str(gift_card.id),
                    "redeem_code": gift_card.redeem_code,
                    "date_of_issue": gift_card.date_of_issue.isoformat(),
                    "date_of_expiry": gift_card.date_of_expiry.isoformat(),
                    "pin": gift_card.pin,
                    "timestamp": gift_card.timestamp.isoformat(),
                    "is_used": gift_card.is_used,
                    "source": gift_card.source,
                    "denomination": gift_card.denomination,
                }
                for gift_card in self.gift_cards
            ],
        }
        self.assertEqual(falcon.HTTP_200, response.status)
        self.assertEqual(expected_body, json.loads(response.text))

    def test_returns_empty_list_when_get(self) -> None:
        request = testing.create_req()
        response = falcon.Response()
        when(self.get_unused_gc_use_case).fetch().thenReturn([])
        self.resource.on_get(request, response)
        expected_body = {
            "status": "ok",
            "data": [],
        }
        self.assertEqual(falcon.HTTP_200, response.status)
        self.assertEqual(expected_body, json.loads(response.text))

    def test_returns_201_when_post(self) -> None:
        payload = GiftCardPayloadFactory()
        request = testing.create_req(body=json.dumps(payload, default=str))
        response = falcon.Response()
        gift_card_create_request = GiftCardCreateRequestFactory(
            redeem_code=payload["redeem_code"],
            date_of_issue=payload["date_of_issue"],
            pin=payload["pin"],
            source=payload["source"],
            denomination=payload["denomination"],
        )
        when(self.create_use_case).create(gift_card_create_request).thenReturn(None)
        self.resource.on_post(request, response)
        self.assertEqual(falcon.HTTP_201, response.status)

    def test_raises_400_when_gift_card_already_exists(self) -> None:
        payload = GiftCardPayloadFactory()
        request = testing.create_req(body=json.dumps(payload, default=str))
        response = falcon.Response()
        gift_card_create_request = GiftCardCreateRequestFactory(
            redeem_code=payload["redeem_code"],
            date_of_issue=payload["date_of_issue"],
            pin=payload["pin"],
            source=payload["source"],
            denomination=payload["denomination"],
        )
        when(self.create_use_case).create(gift_card_create_request).thenRaise(
            GiftCardAlreadyExists,
        )
        with self.assertRaises(errors.HTTPBadRequest):
            self.resource.on_post(request, response)

    def test_raises_400_when_payload_invalid(self) -> None:
        payloads = [
            GiftCardPayloadFactory(redeem_code_length_greater=True),
            GiftCardPayloadFactory(redeem_code_length_lesser=True),
            GiftCardPayloadFactory(redeem_code_not_alphanumeric=True),
            GiftCardPayloadFactory(date_of_issue_one_year_past=True),
            GiftCardPayloadFactory(pin_length_greater=True),
            GiftCardPayloadFactory(pin_length_lesser=True),
            GiftCardPayloadFactory(denomination=9),
            GiftCardPayloadFactory(denomination=10001),
        ]
        for payload in payloads:
            request = testing.create_req(body=json.dumps(payload, default=str))
            response = falcon.Response()
            with self.subTest(payload=payload):
                with self.assertRaises(errors.HTTPBadRequest):
                    self.resource.on_post(request, response)

    def test_returns_200_when_gift_card_updated_successfully(self) -> None:
        update_request = GiftCardUpdateRequestFactory()
        payload = GiftCardPayloadFactory(
            redeem_code=update_request.redeem_code,
            date_of_issue=update_request.date_of_issue.isoformat(),
            pin=update_request.pin,
            source=update_request.source,
            denomination=update_request.denomination,
        )
        request = falcon.testing.create_req(body=json.dumps(payload))
        response = falcon.Response()
        when(self.update_gc_use_case).edit_gc(update_request).thenReturn(None)
        self.resource.on_put(request, response, update_request.id)
        self.assertEqual(falcon.HTTP_200, response.status)

    def test_raises_404_on_update_when_gift_card_not_found(self) -> None:
        update_request = GiftCardUpdateRequestFactory()
        payload = GiftCardPayloadFactory(
            redeem_code=update_request.redeem_code,
            date_of_issue=update_request.date_of_issue.isoformat(),
            pin=update_request.pin,
            source=update_request.source,
            denomination=update_request.denomination,
        )
        request = falcon.testing.create_req(body=json.dumps(payload))
        response = falcon.Response()
        when(self.update_gc_use_case).edit_gc(update_request).thenRaise(
            GiftCardNotFound,
        )
        with self.assertRaises(errors.HTTPNotFound):
            self.resource.on_put(request, response, update_request.id)

    def test_raises_400_on_update_when_gift_card_already_used(self) -> None:
        update_request = GiftCardUpdateRequestFactory()
        payload = GiftCardPayloadFactory(
            redeem_code=update_request.redeem_code,
            date_of_issue=update_request.date_of_issue.isoformat(),
            pin=update_request.pin,
            source=update_request.source,
            denomination=update_request.denomination,
        )
        request = falcon.testing.create_req(body=json.dumps(payload))
        response = falcon.Response()
        when(self.update_gc_use_case).edit_gc(update_request).thenRaise(
            GiftCardAlreadyUsed,
        )
        with self.assertRaises(errors.HTTPBadRequest):
            self.resource.on_put(request, response, update_request.id)

    def test_raises_400_on_update_when_payload_invalid(self) -> None:
        payloads = [
            GiftCardPayloadFactory(redeem_code_length_greater=True),
            GiftCardPayloadFactory(redeem_code_length_lesser=True),
            GiftCardPayloadFactory(redeem_code_not_alphanumeric=True),
            GiftCardPayloadFactory(date_of_issue_one_year_past=True),
            GiftCardPayloadFactory(pin_length_greater=True),
            GiftCardPayloadFactory(pin_length_lesser=True),
            GiftCardPayloadFactory(denomination=9),
            GiftCardPayloadFactory(denomination=10001),
        ]
        for payload in payloads:
            update_request = GiftCardUpdateRequestFactory(
                redeem_code=payload["redeem_code"],
                date_of_issue=payload["date_of_issue"],
                pin=payload["pin"],
                source=payload["source"],
                denomination=payload["denomination"],
            )
            request = testing.create_req(body=json.dumps(payload, default=str))
            response = falcon.Response()
            with self.subTest(payload=payload):
                with self.assertRaises(errors.HTTPBadRequest):
                    self.resource.on_put(request, response, update_request.id)


class TestDenominationResource(TestCase):
    def setUp(self) -> None:
        self.use_case = mock()
        self.resource = DenominationResource(self.use_case)
        self.denominations = [
            Denomination(100),
            Denomination(200),
            Denomination(500),
            Denomination(1000),
            Denomination(5000),
        ]

    def test_returns_expected_denominations(self) -> None:
        request = falcon.testing.create_req()
        response = falcon.Response()
        when(self.use_case).fetch().thenReturn(self.denominations)
        expected_body = {"status": "ok", "data": [100, 200, 500, 1000, 5000]}
        self.resource.on_get(request, response)
        self.assertEqual(falcon.HTTP_200, response.status)
        self.assertEqual(expected_body, json.loads(response.text))

    def test_returns_expected_empty_list(self) -> None:
        request = falcon.testing.create_req()
        response = falcon.Response()
        when(self.use_case).fetch().thenReturn([])
        expected_body = {"status": "ok", "data": []}
        self.resource.on_get(request, response)
        self.assertEqual(falcon.HTTP_200, response.status)
        self.assertEqual(expected_body, json.loads(response.text))


class TestNearExpiryGiftCardResource(TestCase):
    def setUp(self) -> None:
        self.use_case = mock()
        self.resource = NearExpiryGiftCardResource(self.use_case)
        self.gift_card = GiftCardFactory()

    def test_returns_expected_response(self) -> None:
        request = falcon.testing.create_req()
        when(self.use_case).fetch(self.gift_card.denomination).thenReturn(
            self.gift_card,
        )
        response = falcon.Response()
        expected_body = {
            "status": "ok",
            "data": {
                "id": str(self.gift_card.id),
                "redeem_code": self.gift_card.redeem_code,
                "date_of_issue": self.gift_card.date_of_issue.isoformat(),
                "pin": self.gift_card.pin,
                "source": self.gift_card.source,
                "denomination": self.gift_card.denomination,
                "timestamp": self.gift_card.timestamp.isoformat(),
                "is_used": self.gift_card.is_used,
                "date_of_expiry": self.gift_card.date_of_expiry.isoformat(),
            },
        }
        self.resource.on_get(request, response, self.gift_card.denomination)
        self.assertEqual(falcon.HTTP_200, response.status)
        self.assertEqual(expected_body, json.loads(response.text))

    def test_raises_404_when_gift_card_not_found_for_denomination(self) -> None:
        request = falcon.testing.create_req()
        when(self.use_case).fetch(self.gift_card.denomination).thenRaise(
            GiftCardNotFoundForDenomination,
        )
        response = falcon.Response()
        with self.assertRaises(errors.HTTPNotFound):
            self.resource.on_get(request, response, self.gift_card.denomination)


class TestMarkGiftCardUsedResource(TestCase):
    def setUp(self) -> None:
        self.use_case = mock()
        self.resource = MarkGiftCardUsedResource(self.use_case)
        self.gift_card = GiftCardFactory()

    def test_returns_200_when_gift_card_mark_used(self) -> None:
        request = falcon.testing.create_req()
        response = falcon.Response()
        when(self.use_case).mark_used(self.gift_card.id).thenReturn(None)
        self.resource.on_post(request, response, self.gift_card.id)
        self.assertEqual(falcon.HTTP_200, response.status)

    def test_raises_400_when_gift_card_not_found(self) -> None:
        request = falcon.testing.create_req()
        response = falcon.Response()
        when(self.use_case).mark_used(self.gift_card.id).thenRaise(GiftCardNotFound)
        with self.assertRaises(errors.HTTPBadRequest):
            self.resource.on_post(request, response, self.gift_card.id)

    def test_raises_400_when_gift_card_already_used(self) -> None:
        request = falcon.testing.create_req()
        response = falcon.Response()
        when(self.use_case).mark_used(self.gift_card.id).thenRaise(GiftCardAlreadyUsed)
        with self.assertRaises(errors.HTTPBadRequest):
            self.resource.on_post(request, response, self.gift_card.id)
