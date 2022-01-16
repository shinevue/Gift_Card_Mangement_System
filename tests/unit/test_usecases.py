from unittest import TestCase

from mockito import mock
from mockito import verify
from mockito import when

from gcmanager.domain import Denomination
from gcmanager.exceptions import GiftCardAlreadyExists
from gcmanager.usecases import AddGiftCardUseCase
from gcmanager.usecases import DenominationFetcherUseCase
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


class TestDenominationFetcherUseCase(TestCase):
    def setUp(self) -> None:
        self.gc_repository = mock()
        self.use_case = DenominationFetcherUseCase(self.gc_repository)
        self.denominations = [
            Denomination(500),
            Denomination(5000),
            Denomination(100),
            Denomination(200),
        ]

    def test_returns_list_of_denominations_when_called(self) -> None:
        when(self.gc_repository).get_available_denominations().thenReturn(
            self.denominations,
        )
        self.assertEqual(self.denominations, self.use_case.fetch())

    def test_returns_empty_list_of_denominations_when_called(self) -> None:
        when(self.gc_repository).get_available_denominations().thenReturn([])
        self.assertEqual([], self.use_case.fetch())
