from dataclasses import dataclass
from datetime import date
from datetime import datetime
from typing import NewType

Denomination = NewType("Denomination", int)
ReedeemCode = NewType("RedeemCode", str)


@dataclass(frozen=True)
class GiftCard:
    id: str
    redeem_code: ReedeemCode
    date_of_issue: date
    pin: int
    timestamp: datetime
    is_used: bool
    source: str
    denomination: Denomination

    @property
    def date_of_expiry(self) -> date:
        return self.date_of_issue.replace(year=self.date_of_issue.year + 1)
