from flask import jsonify, request

from db import db
from models.category import Categories, category_schema, categories_schema
from util.reflection import populate_object


def add_category():
    post_data = request.form if request.form else request.get_json()

    new_category = Categories.new_category_obj()
    populate_object(new_category, post_data)

    db.session.add(new_category)
    db.session.commit()
    return jsonify({"message": "category created", "result": category_schema.dump(new_category)}), 201


def get_categories():
    category_query = db.session.query(Categories).all()
    if not category_query:
        return jsonify({"message": "no categories found"}), 404
    return jsonify({"message": "categories found", "results": categories_schema.dump(category_query)}), 200


def get_category_by_id(category_id):
    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()
    if not category_query:
        return jsonify({"message": "category not found"}), 404
    return jsonify({"message": "category found", "result": category_schema.dump(category_query)}), 200


def update_category_by_id(category_id):
    post_data = request.form if request.form else request.get_json()
    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()
    if not category_query:
        return jsonify({"message": "category not found"}), 404
    populate_object(category_query, post_data)
    db.session.commit()
    return jsonify({"message": "category updated", "result": category_schema.dump(category_query)}), 200


def delete_category_by_id(category_id):
    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()
    if not category_query:
        return jsonify({"message": "category not found"}), 404
    category_query.products = []
    db.session.delete(category_query)
    db.session.commit()
    return jsonify({"message": "category deleted"}), 200
