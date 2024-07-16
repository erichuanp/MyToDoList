from flask import Blueprint, request, jsonify
from . import db
from .models import User, Task
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import logging
import re

bp = Blueprint('routes', __name__)

def validate_username(username):
    return re.match("^[a-zA-Z0-9_]{3,30}$", username)

def validate_password(password):
    return len(password) >= 6

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"message": "Invalid input"}), 400
    
    if not validate_username(data['username']) or not validate_password(data['password']):
        return jsonify({"message": "Invalid username or password format"}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({"message": "User already exists"}), 400
    
    new_user = User(username=data['username'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    logging.info(f"New user registered: {data['username']}")
    return jsonify({"message": "User registered successfully!"}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.id)
        logging.info(f"User logged in: {data['username']}")
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
    user_id = get_jwt_identity()
    new_task = Task(
        title=data['title'],
        description=data['description'],
        priority=data['priority'],
        due_date=data['due_date'],
        user_id=user_id
    )
    db.session.add(new_task)
    db.session.commit()
    logging.info(f"Task created for user {user_id}: {data['title']}")
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
    logging.info(f"Task updated for user {task.user_id}: {data['title']}")
    return jsonify(task.to_dict()), 200

@bp.route('/tasks/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    logging.info(f"Task deleted for user {task.user_id}: {task.title}")
    return jsonify({"message": "Task deleted"}), 200

@bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify(user_id=user.id, username=user.username), 200

@bp.route('/delete_account', methods=['DELETE'])
@jwt_required()
def delete_account():
    data = request.get_json()
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if user and user.username == data['username'] and user.check_password(data['password']):
        Task.query.filter_by(user_id=user_id).delete()
        db.session.delete(user)
        db.session.commit()
        logging.info(f"User account deleted: {user.username}")
        return jsonify({"message": "Account deleted successfully!"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401
