from flask import jsonify, request

from db import db
from models.warranty import Warranties, warranty_schema, warranties_schema
from models.product import Products
from util.reflection import populate_object


def add_warranty():
    post_data = request.form if request.form else request.get_json()
    new_warranty = Warranties.new_warranty_obj()
    populate_object(new_warranty, post_data)
    db.session.add(new_warranty)
    db.session.commit()
    return jsonify({"message": "warranty created", "result": warranty_schema.dump(new_warranty)}), 201


def get_warranty_by_id(warranty_id):
    warranty_query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()
    if not warranty_query:
        return jsonify({"message": "warranty not found"}), 404
    return jsonify({"message": "warranty found", "result": warranty_schema.dump(warranty_query)}), 200


def update_warranty_by_id(warranty_id):
    post_data = request.form if request.form else request.get_json()
    warranty_query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()
    if not warranty_query:
        return jsonify({"message": "warranty not found"}), 404
    populate_object(warranty_query, post_data)
    db.session.commit()
    return jsonify({"message": "warranty updated", "result": warranty_schema.dump(warranty_query)}), 200


def delete_warranty_by_id(warranty_id):
    warranty_query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()
    if not warranty_query:
        return jsonify({"message": "warranty not found"}), 404

    product_query = db.session.query(Products).filter(Products.product_id == warranty_query.product_id).first()
    if product_query:
        product_query.warranty = None

    db.session.delete(warranty_query)
    db.session.commit()
    return jsonify({"message": "warranty deleted"}), 200
