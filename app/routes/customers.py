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
    """
    ---
    tags:
      - Customers
    summary: Get all customers
    description: Retrieve a list of all customers.
    responses:
      200:
        description: List of customers
        content:
          application/json:
            schema:
              type: array
              items:
                $ref: '#/components/schemas/Customer'
    """
    customers = Customer.query.all()
    return jsonify(customers_schema.dump(customers)), 200

@customers_bp.route('/<int:id>', methods=['GET'])
def get_customer(id):
    """
    ---
    tags:
      - Customers
    summary: Get customer by ID
    description: Retrieve a customer by their ID.
    parameters:
      - in: path
        name: id
        schema:
          type: integer
        required: true
        description: Customer ID
    responses:
      200:
        description: Customer data
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Customer'
      404:
        description: Customer not found
    """
    customer = Customer.query.get_or_404(id)
    return jsonify(customer_schema.dump(customer)), 200

@customers_bp.route('/', methods=['POST'])
@jwt_required()
def create_customer():
    """
    ---
    tags:
      - Customers
    summary: Create a new customer
    description: Create a new customer record. Requires JWT token.
    security:
      - bearerAuth: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/CustomerInput'
    responses:
      201:
        description: Customer created successfully
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Customer'
      400:
        description: Validation errors
      401:
        description: Unauthorized
    """
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
    """
    ---
    tags:
      - Customers
    summary: Update a customer by ID
    description: Update existing customer information. Requires JWT token.
    security:
      - bearerAuth: []
    parameters:
      - in: path
        name: id
        schema:
          type: integer
        required: true
        description: Customer ID
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/CustomerInput'
    responses:
      200:
        description: Customer updated successfully
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Customer'
      400:
        description: Validation errors
      401:
        description: Unauthorized
      404:
        description: Customer not found
    """
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
    """
    ---
    tags:
      - Customers
    summary: Delete a customer by ID
    description: Delete a customer record. Requires JWT token.
    security:
      - bearerAuth: []
    parameters:
      - in: path
        name: id
        schema:
          type: integer
        required: true
        description: Customer ID
    responses:
      204:
        description: Customer deleted successfully, no content returned
      401:
        description: Unauthorized
      404:
        description: Customer not found
    """
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return '', 204
