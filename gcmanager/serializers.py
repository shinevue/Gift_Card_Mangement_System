from typing import Any

from marshmallow import Schema
from marshmallow import fields
from marshmallow import post_load

from gcmanager.domain import GiftCard


class GiftCardAssetSummarySerializer(Schema):
    total = fields.Int()
    used = fields.Int()
    unused = fields.Int()


class GiftCardSerializer(Schema):
    id = fields.UUID(dump_only=True)
    redeem_code = fields.Str()
    date_of_issue = fields.Date()
    pin = fields.Int()
    is_used = fields.Bool(dump_only=True)
    source = fields.Str()
    denomination = fields.Int()
    timestamp = fields.NaiveDateTime(dump_only=True)
    date_of_expiry = fields.Date(dump_only=True)

    @post_load
    def make_gc(self, data: dict, many: bool, **kwargs: Any) -> GiftCard:
        return GiftCard(**data)
