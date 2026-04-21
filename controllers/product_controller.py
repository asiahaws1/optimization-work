from flask import jsonify, request

from db import db
from models.product import Products, product_schema, products_schema
from models.category import Categories
from models.company import Companies
from models.warranty import Warranties
from util.reflection import populate_object

def add_product():
    post_data = request.form if request.form else request.get_json()
    if not post_data:
        return jsonify({"message": "request body required"}), 400
    required_fields = ["product_name", "company_id"]
    missing_fields = [field for field in required_fields if not post_data.get(field)]
    if missing_fields:
        return jsonify({"message": f"missing fields: {', '.join(missing_fields)}"}), 400
    company_query = db.session.query(Companies).filter(Companies.company_id == post_data.get("company_id")).first()
    if not company_query:
        return jsonify({"message": "company not found"}), 404
    new_product = Products.new_product_obj()
    populate_object(new_product, post_data)

    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "product created", "result": product_schema.dump(new_product)}), 201


def add_product_category_association():
    post_data = request.form if request.form else request.get_json()
    product_id = post_data.get("product_id")
    category_id = post_data.get("category_id")

    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()
    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if not product_query or not category_query:
        return jsonify({"message": "product or category not found"}), 404

    if category_query not in product_query.categories:
        product_query.categories.append(category_query)
        db.session.commit()

    return jsonify({"message": "association created", "result": product_schema.dump(product_query)}), 201


def get_products():
    product_query = db.session.query(Products).all()
    if not product_query:
        return jsonify({"message": "no products found"}), 404
    return jsonify({"message": "products found", "results": products_schema.dump(product_query)}), 200


def get_active_products():
    product_query = db.session.query(Products).filter(Products.active.is_(True)).all()
    if not product_query:
        return jsonify({"message": "no active products found"}), 404
    return jsonify({"message": "active products found", "results": products_schema.dump(product_query)}), 200


def get_product_by_id(product_id):
    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()
    if not product_query:
        return jsonify({"message": "product not found"}), 404
    return jsonify({"message": "product found", "result": product_schema.dump(product_query)}), 200


def get_products_by_company_id(company_id):
    company_query = db.session.query(Companies).filter(Companies.company_id == company_id).first()
    if not company_query:
        return jsonify({"message": "company not found"}), 404
    product_query = db.session.query(Products).filter(Products.company_id == company_id).all()
    return jsonify({"message": "products found", "results": products_schema.dump(product_query)}), 200


def update_product_by_id(product_id):
    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()
    post_data = request.form if request.form else request.get_json()

    if product_query:
        populate_object(product_query, post_data)

        db.session.commit()
   
        return jsonify({"message": "product found", "results": product_schema.dump(product_query)}), 200
    
    return jsonify({"message": "unable to update record"}), 400

def delete_product_by_id(product_id):
    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()
    if not product_query:
        return jsonify({"message": "product not found"}), 404

    warranty_query = db.session.query(Warranties).filter(Warranties.product_id == product_id).first()
    if warranty_query:
        db.session.delete(warranty_query)

    product_query.categories = []
    db.session.delete(product_query)
    db.session.commit()
    return jsonify({"message": "product deleted"}), 200