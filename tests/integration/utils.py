from dataclasses import asdict
from datetime import datetime

from gcmanager.domain import GiftCard


def prepare_to_be_inserted_gift_card(gift_card: GiftCard) -> dict:
    serialized_gift_card = asdict(gift_card)
    date_of_issue = serialized_gift_card.pop("date_of_issue")
    serialized_gift_card["date_of_issue"] = datetime(
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
    return serialized_gift_card
