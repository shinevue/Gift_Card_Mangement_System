from gcmanager.domain import Denomination
from gcmanager.domain import GiftCard
from gcmanager.domain import GiftCardAssetSummary
from gcmanager.domain import GiftCardID
from gcmanager.domain import GiftCardUpdateRequest
from gcmanager.exceptions import GiftCardAlreadyExists
from gcmanager.exceptions import GiftCardAlreadyUsed
from gcmanager.exceptions import GiftCardNotFound
from gcmanager.exceptions import GiftCardNotFoundForDenomination
from gcmanager.repositories import GiftCardRepository


class GiftCardAssetInformationUseCase:
    def __init__(self, repository: GiftCardRepository) -> None:
        self._repository = repository

    def summarize(self) -> GiftCardAssetSummary:
        return self._repository.get_summary()


class AddGiftCardUseCase:
    def __init__(self, repository: GiftCardRepository) -> None:
        self._repository = repository

    def create(self, gift_card: GiftCard) -> None:
        if self._repository.get_by_redeem_code(gift_card.redeem_code):
            raise GiftCardAlreadyExists
        self._repository.create(gift_card)


class DenominationFetcherUseCase:
    def __init__(self, repository: GiftCardRepository) -> None:
        self._repository = repository

    def fetch(self) -> list[Denomination]:
        return self._repository.get_available_denominations()


class NearExpiryGiftCardFetcherUseCase:
    def __init__(self, repository: GiftCardRepository) -> None:
        self._repository = repository

    def fetch(self, denomination: Denomination) -> GiftCard:
        gift_card = self._repository.get_near_expiry_gift_card(denomination)
        if not gift_card:
            raise GiftCardNotFoundForDenomination
        return gift_card


class MarkGiftCardUsedUseCase:
    def __init__(self, repository: GiftCardRepository) -> None:
        self._repository = repository

    def mark_used(self, gift_card_id: GiftCardID) -> None:
        if not self._repository.get_by_id(gift_card_id):
            raise GiftCardNotFound
        self._repository.mark_used(gift_card_id)


class EditGiftCardUseCase:
    def __init__(self, repository: GiftCardRepository) -> None:
        self._repository = repository

    def edit_gc(self, request: GiftCardUpdateRequest) -> None:
        gift_card = self._repository.get_by_id(request.id)
        if not gift_card:
            raise GiftCardNotFound
        if gift_card.is_used:
            raise GiftCardAlreadyUsed
        self._repository.update(request)
