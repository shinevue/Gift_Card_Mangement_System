from gcmanager.domain import GiftCardAssetSummary
from gcmanager.repositories import GiftCardRepository


class GiftCardAssetInformationUseCase:
    def __init__(self, repository: GiftCardRepository) -> None:
        self._repository = repository

    def summarize(self) -> GiftCardAssetSummary:
        return self._repository.get_summary()
