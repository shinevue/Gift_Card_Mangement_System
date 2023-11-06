import datetime
import uuid
from abc import ABC
from abc import abstractmethod
from dataclasses import asdict

from pymongo import ASCENDING
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
    ) -> GiftCard | None:
        pass

    @abstractmethod
    def update(self, gift_card_request: GiftCardUpdateRequest) -> None:
        pass

    @abstractmethod
    def mark_used(self, gift_card_id: GiftCardID) -> None:
        pass

    @abstractmethod
    def get_by_id(self, gift_card_id: GiftCardID) -> GiftCard | None:
        pass

    @abstractmethod
    def get_by_redeem_code(self, redeem_code: RedeemCode) -> GiftCard | None:
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
        aggregation_result = list(
            self._collection.aggregate(
                [
                    {
                        "$facet": {
                            "total": [
                                {
                                    "$group": {
                                        "_id": None,
                                        "amount": {"$sum": "$denomination"},
                                    },
                                },
                                {"$project": {"_id": 0}},
                            ],
                            "used": [
                                {"$match": {"is_used": True}},
                                {
                                    "$group": {
                                        "_id": None,
                                        "amount": {"$sum": "$denomination"},
                                    },
                                },
                                {"$project": {"_id": 0}},
                            ],
                        },
                    },
                ],
            ),
        )[0]
        total_aggregation = aggregation_result["total"]
        if not total_aggregation:
            return GiftCardAssetSummary(
                total=Money(0),
                used=Money(0),
            )
        used_aggregation = aggregation_result["used"]
        total = total_aggregation[0]["amount"]
        used = 0 if not used_aggregation else used_aggregation[0]["amount"]
        return GiftCardAssetSummary(total=Money(total), used=Money(used))

    def next_id(self) -> uuid.UUID:
        return uuid.uuid4()

    def timestamp(self) -> datetime.datetime:
        return datetime.datetime.now()

    def get_available_denominations(self) -> list[Denomination]:
        aggregation = self._collection.aggregate(
            [
                {"$match": {"is_used": False}},
                {"$group": {"_id": "$denomination"}},
                {"$sort": {"_id": 1}},
            ],
        )
        return [result["_id"] for result in aggregation]

    def get_near_expiry_gift_card(
        self,
        denomination: Denomination,
    ) -> GiftCard | None:
        result = list(
            self._collection.find({"is_used": False})
            .sort("date_of_issue", ASCENDING)
            .limit(1),
        )
        if not result:
            return None
        gift_card_dict = result[0]
        return self._make_gc(gift_card_dict)

    def update(self, gift_card_request: GiftCardUpdateRequest) -> None:
        date_of_issue = datetime.datetime(
            year=gift_card_request.date_of_issue.year,
            month=gift_card_request.date_of_issue.month,
            day=gift_card_request.date_of_issue.day,
            hour=0,
            minute=0,
            microsecond=0,
        )
        self._collection.update_one(
            {"_id": gift_card_request.id},
            {
                "$set": {
                    "redeem_code": gift_card_request.redeem_code,
                    "pin": gift_card_request.pin,
                    "source": gift_card_request.source,
                    "denomination": gift_card_request.denomination,
                    "date_of_issue": date_of_issue,
                },
            },
        )

    def mark_used(self, gift_card_id: GiftCardID) -> None:
        self._collection.update_one({"_id": gift_card_id}, {"$set": {"is_used": True}})

    def get_by_id(self, gift_card_id: GiftCardID) -> GiftCard | None:
        gc_dict = self._collection.find_one({"_id": gift_card_id})
        if not gc_dict:
            return None
        return self._make_gc(gc_dict)

    @staticmethod
    def _make_gc(gc_dict: dict) -> GiftCard:
        gc_id = gc_dict.pop("_id")
        date_of_issue = gc_dict.pop("date_of_issue").date()
        return GiftCard(**{"id": gc_id, "date_of_issue": date_of_issue, **gc_dict})

    def get_by_redeem_code(self, redeem_code: RedeemCode) -> GiftCard | None:
        gc_dict = self._collection.find_one({"redeem_code": redeem_code})
        if not gc_dict:
            return None
        return self._make_gc(gc_dict)

    def create(self, gift_card: GiftCard) -> None:
        serialized_gift_card = asdict(gift_card)
        date_of_issue = serialized_gift_card.pop("date_of_issue")
        serialized_gift_card["date_of_issue"] = datetime.datetime(
            year=date_of_issue.year,
            month=date_of_issue.month,
            day=date_of_issue.day,
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )
        identity = serialized_gift_card.pop("id")
        serialized_gift_card.update({"_id": identity})
        self._collection.insert_one(serialized_gift_card)

    def get_unused(self) -> list[GiftCard]:
        unused_gift_cards = list(self._collection.find({"is_used": False}))
        return [self._make_gc(gc) for gc in unused_gift_cards]
