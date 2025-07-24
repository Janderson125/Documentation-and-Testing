from flask import Blueprint, request, jsonify
from app.models import Customer
from app.schemas import CustomerSchema
from app import db
from flask_jwt_extended import jwt_required

customers_bp = Blueprint('customers', __name__, url_prefix='/customers')

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

@customers_bp.route('/', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return jsonify(customers_schema.dump(customers)), 200

@customers_bp.route('/<int:id>', methods=['GET'])
def get_customer(id):
    customer = Customer.query.get_or_404(id)
    return jsonify(customer_schema.dump(customer)), 200

@customers_bp.route('/', methods=['POST'])
@jwt_required()
def create_customer():
    data = request.get_json()
    errors = customer_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    customer = Customer(**data)
    db.session.add(customer)
    db.session.commit()
    return jsonify(customer_schema.dump(customer)), 201

@customers_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_customer(id):
    customer = Customer.query.get_or_404(id)
    data = request.get_json()
    errors = customer_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    customer.name = data.get('name', customer.name)
    customer.email = data.get('email', customer.email)
    customer.phone = data.get('phone', customer.phone)
    db.session.commit()
    return jsonify(customer_schema.dump(customer)), 200

@customers_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return '', 204
