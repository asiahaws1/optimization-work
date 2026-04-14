from flask import Blueprint, jsonify, request

import controllers

from models.company import Companies, companies_schema
from db import db

company = Blueprint('company', __name__)

@company.route('/companies', methods=["GET"])

def get_companies():
    company_query = db.session.query(Companies).all()
    
    if not company_query:
        return jsonify({"message": "no companies found"}), 404
    
    else:
      return jsonify({"message": "companies found", "results": companies_schema.dump(company_query)}), 200
    

@company.route('/company', methods=["POST"])
def add_company():
   return controllers.add_company()


@company.route('/company/<company_id>', methods=["PUT"])
def update_company_by_id(company_id):
   return controllers.update_company_by_id(company_id)


@company.route('/company/<company_id>', methods=["GET"])
def get_company_by_id(company_id):
   return controllers.get_company_by_id(company_id)


@company.route('/company/delete/<company_id>', methods=["DELETE"])
def delete_company_by_id(company_id):
   return controllers.delete_company_by_id(company_id)


companies = company