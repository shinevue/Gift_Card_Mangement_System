from abc import ABC
from abc import abstractmethod

from gcmanager.domain import Denomination
from gcmanager.domain import GiftCard
from gcmanager.domain import GiftCardAssetSummary
from gcmanager.domain import GiftCardID


class GiftCardRepository(ABC):
    @abstractmethod
    def get_available_denominations(self) -> list[Denomination]:
        pass

    @abstractmethod
    def get_near_expiry_gift_card(self, denomination: Denomination) -> GiftCard:
        pass

    @abstractmethod
    def update(self, gift_card: GiftCard) -> None:
        pass

    @abstractmethod
    def get(self, gift_card_id: GiftCardID) -> GiftCard:
        pass

    @abstractmethod
    def create(self, gift_card: GiftCard) -> None:
        pass

    @abstractmethod
    def get_unused(self) -> list[GiftCard]:
        pass

    @abstractmethod
    def get_summary(self) -> GiftCardAssetSummary:
        pass
