from gcmanager.domain import Denomination
from gcmanager.domain import GiftCard
from gcmanager.domain import GiftCardAssetSummary
from gcmanager.exceptions import GiftCardAlreadyExists
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
