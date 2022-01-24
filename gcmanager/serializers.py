from marshmallow import Schema
from marshmallow import fields


class GiftCardAssetSummarySerializer(Schema):
    total = fields.Int()
    used = fields.Int()
    unused = fields.Int()


class GiftCardSerializer(Schema):
    id = fields.Str()
    redeem_code = fields.Str()
    date_of_issue = fields.Date()
    pin = fields.Int()
    is_used = fields.Bool()
    source = fields.Str()
    denomination = fields.Int()
    timestamp = fields.NaiveDateTime()
    date_of_expiry = fields.Date()
