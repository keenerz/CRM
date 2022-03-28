"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Todos
from api.utils import generate_sitemap, APIException
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

api = Blueprint('api', __name__)


#Token Endpoints
@api.route('/token', methods=['POST'])
def create_token():
    if request.json is None:
        return jsonify({"msg":"Missing the payload"}), 400
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    user = User.query.filter_by(email=email, password=password).first()
    if user is None:
        return jsonify({"msg": "Missing email or password"}), 401
    access_token = create_access_token(identity=user.id)
    return jsonify({ "token": access_token, "user_id": user.id, "usertype": user.usertype })

#User Endpoints
@api.route('/user', methods=['GET'])
@jwt_required()
def get_user():
    current_user_id = get_jwt_identity()
    user_query = User.query.filter_by(id=current_user_id).first()
    if user_query is None:
        return jsonify({"msg": "User Not Found"}), 403
    email_get = user_query.email
    username_get = user_query.username
    return jsonify({"email": email_get, "username": username_get})

#Todo Endpoints
@api.route('/todos', methods=['POST'])
@jwt_required()
def create_todos():
    todos = request.json.get('todos', None)
    creator = get_jwt_identity()
    todo_type = request.json.get('todo_type', None)
    stage = request.json.get('stage', None)
    acceptance = request.json.get('acceptance', None)
    due_date = request.json.get('due_date', None)
    details = request.json.get('details', None)
    
    todos = Todos(todos=todos,
                    project_type=project_type,
                    creator=creator,
                    todo_type=todo_type,
                    stage=stage,
                    acceptance=acceptance,
                    due_date=due_date,
                    details=details)
    db.session.add(todos)
    db.session.commit()
    return jsonify(project.serialize())