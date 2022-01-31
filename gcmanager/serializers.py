from typing import Any

from marshmallow import Schema
from marshmallow import fields
from marshmallow import post_load
from marshmallow import validate

from gcmanager.domain import GiftCardCreateRequest
from gcmanager.validators import date_not_more_than_equal_to_a_year_old


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


class GiftCardCreateRequestSerializer(Schema):
    redeem_code = fields.Str(
        required=True,
        validate=[validate.Length(equal=14), validate.Regexp(r"[A-Z0-9]{14}")],
    )
    date_of_issue = fields.Date(
        required=True,
        validate=[date_not_more_than_equal_to_a_year_old],
    )
    pin = fields.Int(
        required=True,
        validate=[validate.Range(min=1_000_000_000_000_000, max=9_999_999_999_999_999)],
    )
    source = fields.Str(required=True)
    denomination = fields.Int(
        required=True,
        validate=[validate.Range(min=10, max=10_000)],
    )

    @post_load
    def make_request(
        self,
        data: dict,
        many: bool,
        **kwargs: Any,
    ) -> GiftCardCreateRequest:
        return GiftCardCreateRequest(**data)
