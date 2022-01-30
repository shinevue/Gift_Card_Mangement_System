import json
from unittest import TestCase

import falcon
from falcon import testing
from mockito import mock
from mockito import when

from gcmanager.domain import GiftCardAssetSummary
from gcmanager.domain import Money
from gcmanager.webapi import GiftCardAssetInformationResource
from gcmanager.webapi import GiftCardResource
from tests.unit.factories import GiftCardCreateRequestFactory
from tests.unit.factories import GiftCardFactory
from tests.unit.factories import GiftCardPayloadFactory


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
        self.maxDiff = None
        self.create_use_case = mock()
        self.get_unused_gc_use_case = mock()
        self.resource = GiftCardResource(
            self.create_use_case,
            self.get_unused_gc_use_case,
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
