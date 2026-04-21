import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db
from models.product_category_xref import products_categories_association_table


class Products(db.Model):
    __tablename__ = 'Products'

    product_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_name = db.Column(db.String(), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    company_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Companies.company_id'), nullable=False)

    company = db.relationship('Companies', back_populates='products')
    categories = db.relationship('Categories', secondary=products_categories_association_table, back_populates='products')
    warranty = db.relationship('Warranties', back_populates='product', uselist=False)

    def __init__(self, product_name, company_id, active=True):
        self.product_name = product_name
        self.company_id = company_id
        self.active = active


    def new_product_obj():
        return Products('', '', True)


class ProductsSchema(ma.Schema):
    class Meta:
        fields = ['product_id', 'product_name', 'active', 'company_id', 'company', 'categories', 'warranty']

    product_id = ma.fields.UUID()
    product_name = ma.fields.String(required=True)
    active = ma.fields.Boolean(required=True, dump_default=True)
    company_id = ma.fields.UUID(required=True)

    company = ma.fields.Nested('CompaniesSchema', exclude=['products'])
    categories = ma.fields.Nested('CategoriesSchema', many=True)
    warranty = ma.fields.Nested('WarrantiesSchema', exclude=['product'])


product_schema = ProductsSchema()
products_schema = ProductsSchema(many=True)
