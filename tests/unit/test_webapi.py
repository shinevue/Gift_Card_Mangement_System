import json
from unittest import TestCase

import falcon
from falcon import testing
from mockito import mock
from mockito import when

from gcmanager.domain import GiftCardAssetSummary
from gcmanager.domain import Money
from gcmanager.webapi import GiftCardAssetInformationResource


class TestGiftCardAssetInformationResource(TestCase):
    def setUp(self) -> None:
        self.use_case = mock()
        self.resource = GiftCardAssetInformationResource(self.use_case)

    def test_returns_expected_response(self) -> None:
        when(self.use_case).summarize().thenReturn(
            GiftCardAssetSummary(total=Money(1000), used=Money(800)),
        )
        self.request = testing.create_req()
        self.response = falcon.Response()
        self.resource.on_get(self.request, self.response)
        expected_body = {
            "status": "ok",
            "data": {
                "total": 1000,
                "used": 800,
                "unused": 200,
            },
        }
        self.assertEqual(falcon.HTTP_200, self.response.status)
        self.assertEqual(expected_body, json.loads(self.response.text))
