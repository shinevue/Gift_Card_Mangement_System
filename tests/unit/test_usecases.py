from unittest import TestCase

from mockito import mock
from mockito import verify
from mockito import when

from gcmanager.domain import Denomination
from gcmanager.exceptions import GiftCardAlreadyExists
from gcmanager.exceptions import GiftCardAlreadyUsed
from gcmanager.exceptions import GiftCardNotFound
from gcmanager.exceptions import GiftCardNotFoundForDenomination
from gcmanager.usecases import AddGiftCardUseCase
from gcmanager.usecases import DenominationFetcherUseCase
from gcmanager.usecases import EditGiftCardUseCase
from gcmanager.usecases import FetchUnusedGiftCardsUseCase
from gcmanager.usecases import GiftCardAssetInformationUseCase
from gcmanager.usecases import MarkGiftCardUsedUseCase
from gcmanager.usecases import NearExpiryGiftCardFetcherUseCase
from tests.unit.factories import GiftCardAssetSummaryFactory
from tests.unit.factories import GiftCardCreateRequestFactory
from tests.unit.factories import GiftCardFactory
from tests.unit.factories import GiftCardUpdateRequestFactory


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
        self.gift_card_create_request = GiftCardCreateRequestFactory()
        self.gift_card = GiftCardFactory(
            redeem_code=self.gift_card_create_request.redeem_code,
            date_of_issue=self.gift_card_create_request.date_of_issue,
            pin=self.gift_card_create_request.pin,
            source=self.gift_card_create_request.source,
            denomination=self.gift_card_create_request.denomination,
        )

    def test_returns_none_when_gift_card_created(self) -> None:
        when(self.gc_repository).get_by_redeem_code(
            self.gift_card_create_request.redeem_code,
        ).thenReturn(None)
        when(self.gc_repository).create(self.gift_card).thenReturn(None)
        when(self.gc_repository).next_id().thenReturn(self.gift_card.id)
        when(self.gc_repository).timestamp().thenReturn(self.gift_card.timestamp)
        self.use_case.create(self.gift_card_create_request)
        verify(self.gc_repository).create(self.gift_card)

    def test_raises_when_gift_card_already_exists(self) -> None:
        when(self.gc_repository).get_by_redeem_code(
            self.gift_card_create_request.redeem_code,
        ).thenReturn(
            self.gift_card,
        )
        with self.assertRaises(GiftCardAlreadyExists):
            self.use_case.create(self.gift_card_create_request)


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


class TestNearExpiryGiftCardFetcherUseCase(TestCase):
    def setUp(self) -> None:
        self.gc_repository = mock()
        self.use_case = NearExpiryGiftCardFetcherUseCase(self.gc_repository)
        self.gift_card = GiftCardFactory()

    def test_returns_gift_card_when_fetched(self) -> None:
        when(self.gc_repository).get_near_expiry_gift_card(
            self.gift_card.denomination,
        ).thenReturn(self.gift_card)
        actual = self.use_case.fetch(self.gift_card.denomination)
        self.assertEqual(self.gift_card, actual)

    def test_raises_when_gift_card_not_found(self) -> None:
        when(self.gc_repository).get_near_expiry_gift_card(
            self.gift_card.denomination,
        ).thenReturn(None)
        with self.assertRaises(GiftCardNotFoundForDenomination):
            self.use_case.fetch(self.gift_card.denomination)


class TestMarkGiftCardUsedUseCase(TestCase):
    def setUp(self) -> None:
        self.gc_repository = mock()
        self.use_case = MarkGiftCardUsedUseCase(self.gc_repository)

    def test_marks_gift_card_as_used_when_called(self) -> None:
        gift_card = GiftCardFactory()
        when(self.gc_repository).get_by_id(gift_card.id).thenReturn(gift_card)
        when(self.gc_repository).mark_used(gift_card.id).thenReturn(None)
        self.use_case.mark_used(gift_card.id)
        verify(self.gc_repository).mark_used(gift_card.id)

    def test_raises_when_gift_card_is_not_found(self) -> None:
        gift_card = GiftCardFactory()
        when(self.gc_repository).get_by_id(gift_card.id).thenReturn(None)
        with self.assertRaises(GiftCardNotFound):
            self.use_case.mark_used(gift_card.id)


class TestEditGiftCardUseCase(TestCase):
    def setUp(self) -> None:
        self.gc_repository = mock()
        self.use_case = EditGiftCardUseCase(self.gc_repository)

    def test_returns_none_when_gift_card_updated(self) -> None:
        gift_card = GiftCardFactory()
        gift_card_update_request = GiftCardUpdateRequestFactory(id=gift_card.id)
        when(self.gc_repository).get_by_id(gift_card.id).thenReturn(gift_card)
        when(self.gc_repository).update(gift_card_update_request).thenReturn(None)
        self.use_case.edit_gc(gift_card_update_request)

    def test_raises_when_gift_card_not_found(self) -> None:
        gift_card = GiftCardFactory()
        gift_card_update_request = GiftCardUpdateRequestFactory(id=gift_card.id)
        when(self.gc_repository).get_by_id(gift_card.id).thenReturn(None)
        with self.assertRaises(GiftCardNotFound):
            self.use_case.edit_gc(gift_card_update_request)

    def test_raises_when_gift_card_is_used(self) -> None:
        gift_card = GiftCardFactory(is_used=True)
        gift_card_update_request = GiftCardUpdateRequestFactory(id=gift_card.id)
        when(self.gc_repository).get_by_id(gift_card.id).thenReturn(gift_card)
        with self.assertRaises(GiftCardAlreadyUsed):
            self.use_case.edit_gc(gift_card_update_request)


class TestFetchUnusedGiftCardsUseCase(TestCase):
    def setUp(self) -> None:
        self.gc_repository = mock()
        self.use_case = FetchUnusedGiftCardsUseCase(self.gc_repository)
        self.gift_cards = GiftCardFactory.build_batch(size=4, is_used=False)

    def test_returns_unused_gift_cards_when_called(self) -> None:
        when(self.gc_repository).get_unused().thenReturn(self.gift_cards)
        actual = self.use_case.fetch()
        self.assertEqual(self.gift_cards, actual)

    def test_returns_empty_list_when_called(self) -> None:
        when(self.gc_repository).get_unused().thenReturn([])
        actual = self.use_case.fetch()
        self.assertEqual([], actual)
