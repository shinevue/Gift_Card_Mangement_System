import datetime
import uuid
from abc import ABC
from abc import abstractmethod
from typing import Optional

from pymongo.collection import Collection

from gcmanager.domain import Denomination
from gcmanager.domain import GiftCard
from gcmanager.domain import GiftCardAssetSummary
from gcmanager.domain import GiftCardID
from gcmanager.domain import GiftCardUpdateRequest
from gcmanager.domain import RedeemCode


class GiftCardRepository(ABC):
    @abstractmethod
    def next_id(self) -> uuid.UUID:
        pass

    @abstractmethod
    def timestamp(self) -> datetime.datetime:
        pass

    @abstractmethod
    def get_available_denominations(self) -> list[Denomination]:
        pass

    @abstractmethod
    def get_near_expiry_gift_card(
        self,
        denomination: Denomination,
    ) -> Optional[GiftCard]:
        pass

    @abstractmethod
    def update(self, gift_card_request: GiftCardUpdateRequest) -> None:
        pass

    @abstractmethod
    def mark_used(self, gift_card_id: GiftCardID) -> None:
        pass

    @abstractmethod
    def get_by_id(self, gift_card_id: GiftCardID) -> Optional[GiftCard]:
        pass

    @abstractmethod
    def get_by_redeem_code(self, redeem_code: RedeemCode) -> Optional[GiftCard]:
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


class GiftCardMongoDBRepository(GiftCardRepository):
    def __init__(self, gc_collection: Collection) -> None:
        self._collection = gc_collection

    def get_summary(self) -> GiftCardAssetSummary:
        pass

    def next_id(self) -> uuid.UUID:
        pass

    def timestamp(self) -> datetime.datetime:
        pass

    def get_available_denominations(self) -> list[Denomination]:
        pass

    def get_near_expiry_gift_card(
        self,
        denomination: Denomination,
    ) -> Optional[GiftCard]:
        pass

    def update(self, gift_card_request: GiftCardUpdateRequest) -> None:
        pass

    def mark_used(self, gift_card_id: GiftCardID) -> None:
        pass

    def get_by_id(self, gift_card_id: GiftCardID) -> Optional[GiftCard]:
        pass

    def get_by_redeem_code(self, redeem_code: RedeemCode) -> Optional[GiftCard]:
        pass

    def create(self, gift_card: GiftCard) -> None:
        pass

    def get_unused(self) -> list[GiftCard]:
        pass
