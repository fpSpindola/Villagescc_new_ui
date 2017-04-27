from marshmallow.schema import Schema
from marshmallow.validate import OneOf, Range
from marshmallow import fields
from listings.models import LISTING_TYPE


class SubmitListingSchema(Schema):

    listing_type = fields.Integer(validate=[OneOf(list(LISTING_TYPE))], required=True)
    title = fields.String(required=True)
    description = fields.String(required=False)
    price = fields.Integer(required=True, default=0, validate=[Range(min=0, max=999)])
    subcategories = fields.String(required=True)
    photo = fields.String(required=False)
