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
from gcmanager.domain import Money
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
        total_aggregation = list(
            self._collection.aggregate(
                [
                    {"$group": {"_id": None, "total": {"$sum": "$denomination"}}},
                    {"$project": {"_id": 0}},
                ],
            ),
        )

        if not total_aggregation:
            return GiftCardAssetSummary(
                total=Money(0),
                used=Money(0),
            )

        used_aggregation = list(
            self._collection.aggregate(
                [
                    {"$match": {"is_used": True}},
                    {"$group": {"_id": None, "used": {"$sum": "$denomination"}}},
                    {"$project": {"_id": 0}},
                ],
            ),
        )

        total = total_aggregation[0]["total"]
        if not used_aggregation:
            used = 0
        else:
            used = used_aggregation[0]["used"]

        return GiftCardAssetSummary(total=Money(total), used=Money(used))

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
        self._collection.update_one({"_id": gift_card_id}, {"$set": {"is_used": True}})

    def get_by_id(self, gift_card_id: GiftCardID) -> Optional[GiftCard]:
        gc_dict = self._collection.find_one({"_id": gift_card_id})
        if not gc_dict:
            return None
        gc_id = gc_dict.pop("_id")
        date_of_issue = gc_dict.pop("date_of_issue").date()
        return GiftCard(**{"id": gc_id, "date_of_issue": date_of_issue, **gc_dict})

    def get_by_redeem_code(self, redeem_code: RedeemCode) -> Optional[GiftCard]:
        pass

    def create(self, gift_card: GiftCard) -> None:
        pass

    def get_unused(self) -> list[GiftCard]:
        pass
