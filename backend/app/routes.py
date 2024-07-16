from flask import Blueprint, request, jsonify
from . import db
from .models import User, Task
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

bp = Blueprint('routes', __name__)

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    new_user = User(username=data['username'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!"}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.password == data['password']:
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    return jsonify({"message": "Invalid credentials"}), 401

@bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()
    tasks = Task.query.filter_by(user_id=user_id).all()
    return jsonify([task.to_dict() for task in tasks]), 200

@bp.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    data = request.get_json()
    print("Received task data:", data)
    user_id = get_jwt_identity()
    print("Authenticated user ID:", user_id)
    new_task = Task(
        title=data['title'],
        description=data['description'],
        priority=data['priority'],
        due_date=data['due_date'],
        user_id=user_id
    )
    db.session.add(new_task)
    db.session.commit()
    print("Task created successfully")
    return jsonify(new_task.to_dict()), 201

@bp.route('/tasks/<int:id>', methods=['PUT'])
@jwt_required()
def update_task(id):
    data = request.get_json()
    task = Task.query.get_or_404(id)
    task.title = data['title']
    task.description = data['description']
    task.priority = data['priority']
    task.due_date = data['due_date']
    db.session.commit()
    return jsonify(task.to_dict()), 200

@bp.route('/tasks/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"}), 200
