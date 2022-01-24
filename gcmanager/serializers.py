from marshmallow import Schema
from marshmallow import fields


class GiftCardAssetSummarySerializer(Schema):
    total = fields.Int()
    used = fields.Int()
    unused = fields.Int()
