from flask import jsonify, request

from models.company import Companies, company_schema, companies_schema
from models.product import Products
from models.warranty import Warranties
from util.reflection import populate_object
from db import db


def get_companies():
    company_query = db.session.query(Companies).all()

    if not company_query:
        return jsonify({"message": "no companies found"}), 404

    return jsonify({"message": "companies found", "results": companies_schema.dump(company_query)}), 200


def add_company():
    post_data = request.form if request.form else request.json

    new_company = Companies(company_name=post_data.get("company_name"))

    db.session.add(new_company)
    db.session.commit()

    return jsonify({"message": "company created", "result": company_schema.dump(new_company)}), 201


def update_company_by_id(company_id):
    post_data = request.form if request.form else request.json
    company_query = db.session.query(Companies).filter(Companies.company_id == company_id).first()

    if not company_query:
        return jsonify({"message": "company not found"}), 404
    
    populate_object(company_query, post_data)

    db.session.commit()

    return jsonify({"message": "company updated", "result": company_schema.dump(company_query)}), 200


def get_company_by_id(company_id):
    company_query = db.session.query(Companies).filter(Companies.company_id == company_id).first()
    if not company_query:
        return jsonify({"message": "company not found"}), 404
    return jsonify({"message": "company found", "result": company_schema.dump(company_query)}), 200


def delete_company_by_id(company_id):
    company_query = db.session.query(Companies).filter(Companies.company_id == company_id).first()
    if not company_query:
        return jsonify({"message": "company not found"}), 404

    for product in list(company_query.products):
        warranty_query = db.session.query(Warranties).filter(Warranties.product_id == product.product_id).first()
        if warranty_query:
            db.session.delete(warranty_query)
        product.categories = []
        db.session.delete(product)

    db.session.delete(company_query)
    db.session.commit()
    return jsonify({"message": "company deleted"}), 200