from app import ma
from marshmallow import fields, validate

class MechanicSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))
    specialty = fields.Str(required=True, validate=validate.Length(min=1))
    phone = fields.Str()

class CustomerSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))
    email = fields.Email(required=True)
    phone = fields.Str()
