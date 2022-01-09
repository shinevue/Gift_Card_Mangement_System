from dataclasses import dataclass
from datetime import date
from datetime import datetime
from typing import NewType

Denomination = NewType("Denomination", int)
RedeemCode = NewType("RedeemCode", str)
GiftCardID = NewType("GiftCardID", str)
Money = NewType("Money", int)


@dataclass(frozen=True)
class GiftCard:
    id: GiftCardID
    redeem_code: RedeemCode
    date_of_issue: date
    pin: int
    timestamp: datetime
    is_used: bool
    source: str
    denomination: Denomination

    @property
    def date_of_expiry(self) -> date:
        return self.date_of_issue.replace(year=self.date_of_issue.year + 1)


@dataclass(frozen=True)
class GiftCardAssetSummary:
    total: Money
    used: Money

    @property
    def unused(self) -> Money:
        return Money(self.total - self.used)
