import uuid
from sqlalchemy.dialects.postgresql import UUID
from marshmallow import Schema, fields

from db import db


class Warranties(db.Model):
    __tablename__ = "Warranties"

    warranty_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Products.product_id"), unique=True)
    length_months = db.Column(db.Integer())
    description = db.Column(db.String())

    product = db.relationship("Products", back_populates="warranty")

    def __init__(self, product_id, length_months=None, description=None):
        self.product_id = product_id
        self.length_months = length_months
        self.description = description


class WarrantySchema(Schema):
    warranty_id = fields.String()
    product_id = fields.String()
    length_months = fields.Integer()
    description = fields.String()


warranty_schema = WarrantySchema()
warranties_schema = WarrantySchema(many=True)
