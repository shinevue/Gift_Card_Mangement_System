from tests.integration.db_app_test_case import MongoDBAndAppAwareTestCase


class TestGiftCardAssetInformationAPI(MongoDBAndAppAwareTestCase):
    def setUp(self) -> None:
        super(TestGiftCardAssetInformationAPI, self).setUp()
        self.api_path = "/api/giftcards/assets/"

    def test_returns_zero_for_all_when_db_empty(self) -> None:
        self.simulate_get(self.api_path)
