import uuid
from sqlalchemy.dialects.postgresql import UUID
from marshmallow import Schema, fields

from db import db
from models.product_category_xref import products_categories_association_table


class Products(db.Model):
    __tablename__ = "Products"

    product_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_name = db.Column(db.String(), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    company_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Companies.company_id"), nullable=False)

    company = db.relationship("Companies", back_populates="products")
    categories = db.relationship("Categories", secondary=products_categories_association_table, back_populates="products")
    warranty = db.relationship("Warranties", back_populates="product", uselist=False)

    def __init__(self, product_name, company_id, active=True):
        self.product_name = product_name
        self.company_id = company_id
        self.active = active


class _CategoryNested(Schema):
    category_id = fields.String()
    category_name = fields.String()


class _WarrantyNested(Schema):
    warranty_id = fields.String()
    product_id = fields.String()
    length_months = fields.Integer()
    description = fields.String()


class ProductSchema(Schema):
    product_id = fields.String()
    product_name = fields.String()
    active = fields.Boolean()
    company_id = fields.String()
    categories = fields.List(fields.Nested(_CategoryNested))
    warranty = fields.Nested(_WarrantyNested, allow_none=True)


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
