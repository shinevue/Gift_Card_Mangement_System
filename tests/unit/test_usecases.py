from unittest import TestCase
from unittest.mock import Mock

from gcmanager.usecases import GiftCardAssetInformationUseCase
from tests.unit.factories import GiftCardAssetSummaryFactory


class TestGiftCardAssetInformationUseCase(TestCase):
    def setUp(self) -> None:
        self.gc_repository = Mock()
        self.asset_info = GiftCardAssetSummaryFactory()
        self.gc_repository.get_summary = Mock(return_value=self.asset_info)
        self.use_case = GiftCardAssetInformationUseCase(self.gc_repository)

    def test_returns_asset_information_when_called(self) -> None:
        actual_asset_information = self.use_case.summarize()
        self.assertEqual(self.asset_info, actual_asset_information)
