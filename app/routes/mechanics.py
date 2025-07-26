from flask import Blueprint, request, jsonify
from app.models import Mechanic
from app.schemas import MechanicSchema
from app import db
from flask_jwt_extended import jwt_required

mechanics_bp = Blueprint('mechanics', __name__, url_prefix='/mechanics')

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)

@mechanics_bp.route('/', methods=['GET'])
def get_mechanics():
    """
    ---
    tags:
      - Mechanics
    summary: Get all mechanics
    description: Retrieve a list of all mechanics.
    responses:
      200:
        description: List of mechanics
        content:
          application/json:
            schema:
              type: array
              items:
                $ref: '#/components/schemas/Mechanic'
    """
    mechanics = Mechanic.query.all()
    return jsonify(mechanics_schema.dump(mechanics)), 200

@mechanics_bp.route('/<int:id>', methods=['GET'])
def get_mechanic(id):
    """
    ---
    tags:
      - Mechanics
    summary: Get mechanic by ID
    description: Retrieve a mechanic by their ID.
    parameters:
      - in: path
        name: id
        schema:
          type: integer
        required: true
        description: Mechanic ID
    responses:
      200:
        description: Mechanic data
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Mechanic'
      404:
        description: Mechanic not found
    """
    mechanic = Mechanic.query.get_or_404(id)
    return mechanic_schema.jsonify(mechanic), 200

@mechanics_bp.route('/', methods=['POST'])
@jwt_required()
def create_mechanic():
    """
    ---
    tags:
      - Mechanics
    summary: Create a new mechanic
    description: Create a new mechanic record. Requires JWT token.
    security:
      - bearerAuth: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/MechanicInput'
    responses:
      201:
        description: Mechanic created successfully
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Mechanic'
      400:
        description: Validation errors
      401:
        description: Unauthorized (missing or invalid token)
    """
    data = request.get_json()
    errors = mechanic_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    mechanic = Mechanic(**data)
    db.session.add(mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 201

@mechanics_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_mechanic(id):
    """
    ---
    tags:
      - Mechanics
    summary: Update a mechanic by ID
    description: Update existing mechanic information. Requires JWT token.
    security:
      - bearerAuth: []
    parameters:
      - in: path
        name: id
        schema:
          type: integer
        required: true
        description: Mechanic ID
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/MechanicInput'
    responses:
      200:
        description: Mechanic updated successfully
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Mechanic'
      400:
        description: Validation errors
      401:
        description: Unauthorized (missing or invalid token)
      404:
        description: Mechanic not found
    """
    mechanic = Mechanic.query.get_or_404(id)
    data = request.get_json()
    errors = mechanic_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    mechanic.name = data['name']
    mechanic.specialty = data['specialty']
    mechanic.phone = data.get('phone')
    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200

@mechanics_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_mechanic(id):
    """
    ---
    tags:
      - Mechanics
    summary: Delete a mechanic by ID
    description: Delete a mechanic record. Requires JWT token.
    security:
      - bearerAuth: []
    parameters:
      - in: path
        name: id
        schema:
          type: integer
        required: true
        description: Mechanic ID
    responses:
      204:
        description: Mechanic deleted successfully, no content returned
      401:
        description: Unauthorized (missing or invalid token)
      404:
        description: Mechanic not found
    """
    mechanic = Mechanic.query.get_or_404(id)
    db.session.delete(mechanic)
    db.session.commit()
    return '', 204
