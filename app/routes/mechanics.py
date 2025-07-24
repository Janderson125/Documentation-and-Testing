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
    mechanics = Mechanic.query.all()
    return jsonify(mechanics_schema.dump(mechanics)), 200

@mechanics_bp.route('/<int:id>', methods=['GET'])
def get_mechanic(id):
    mechanic = Mechanic.query.get_or_404(id)
    return mechanic_schema.jsonify(mechanic), 200

@mechanics_bp.route('/', methods=['POST'])
@jwt_required()
def create_mechanic():
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
    mechanic = Mechanic.query.get_or_404(id)
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": "Deleted"}), 204
