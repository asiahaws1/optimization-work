import uuid
from sqlalchemy.dialects.postgresql import UUID
from marshmallow import Schema, fields

from db import db


class Companies(db.Model):
    __tablename__ = "Companies"

    company_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_name = db.Column(db.String(), nullable=False)

    products = db.relationship("Products", back_populates="company")

    def __init__(self, company_name):
        self.company_name = company_name


class CompanySchema(Schema):
    company_id = fields.String()
    company_name = fields.String()


company_schema = CompanySchema()
companies_schema = CompanySchema(many=True)
