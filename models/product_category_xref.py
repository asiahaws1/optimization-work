from sqlalchemy.dialects.postgresql import UUID

from db import db


products_categories_association_table = db.Table(
    "products_categories",
    db.Column("product_id", UUID(as_uuid=True), db.ForeignKey("Products.product_id"), primary_key=True),
    db.Column("category_id", UUID(as_uuid=True), db.ForeignKey("Categories.category_id"), primary_key=True),
)
