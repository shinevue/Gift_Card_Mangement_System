from unittest import TestCase

from mockito import mock
from mockito import verify
from mockito import when

from gcmanager.exceptions import GiftCardAlreadyExists
from gcmanager.usecases import AddGiftCardUseCase
from gcmanager.usecases import GiftCardAssetInformationUseCase
from tests.unit.factories import GiftCardAssetSummaryFactory
from tests.unit.factories import GiftCardFactory


class TestGiftCardAssetInformationUseCase(TestCase):
    def setUp(self) -> None:
        self.gc_repository = mock()
        self.asset_info = GiftCardAssetSummaryFactory()
        when(self.gc_repository).get_summary().thenReturn(self.asset_info)
        self.use_case = GiftCardAssetInformationUseCase(self.gc_repository)

    def test_returns_asset_information_when_called(self) -> None:
        actual_asset_information = self.use_case.summarize()
        self.assertEqual(self.asset_info, actual_asset_information)


class TestAddGiftCardUseCase(TestCase):
    def setUp(self) -> None:
        self.gc_repository = mock()
        self.use_case = AddGiftCardUseCase(self.gc_repository)
        self.gift_card = GiftCardFactory()

    def test_returns_none_when_gift_card_created(self) -> None:
        when(self.gc_repository).get_by_redeem_code(
            self.gift_card.redeem_code,
        ).thenReturn(None)
        when(self.gc_repository).create(self.gift_card).thenReturn(None)
        self.use_case.create(self.gift_card)
        verify(self.gc_repository).create(self.gift_card)

    def test_raises_when_gift_card_already_exists(self) -> None:
        gift_card = GiftCardFactory()
        when(self.gc_repository).get_by_redeem_code(gift_card.redeem_code).thenReturn(
            gift_card,
        )
        with self.assertRaises(GiftCardAlreadyExists):
            self.use_case.create(gift_card)
