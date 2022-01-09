from dataclasses import dataclass
from datetime import date
from datetime import datetime
from typing import NewType

Denomination = NewType("Denomination", int)
RedeemCode = NewType("RedeemCode", str)


@dataclass(frozen=True)
class GiftCard:
    id: str
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
    total: Denomination
    used: Denomination

    @property
    def unused(self) -> Denomination:
        return Denomination(self.total - self.used)
