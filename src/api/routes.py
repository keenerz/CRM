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
                    todo_type=todo_type,
                    creator=creator,
                    stage=stage,
                    acceptance=acceptance,
                    due_date=due_date,
                    details=details)
    db.session.add(todos)
    db.session.commit()
    return jsonify(project.serialize())

@api.route('/todos', methods=['PUT'])
@jwt_required()
def update_todo():
    todoid = request.json.get('id')
    todo = Todos.query.filter_by(id=todoid).first()
    if todo is None:
        return jsonify({"msg":"Item doesn't exist"}), 400
    todos = request.json.get('todos')
    todo_type = request.json.get('todo_type')
    stage = request.json.get('stage')
    acceptance = request.json.get('acceptance')
    due_date = request.json.get('due_date')
    details = request.json.get('details')

    if todos is None or not todos:
        todo.todos = todo.todos
    else:
        todo.todos = todos

    if todo_type is None or not todo_type:
        todo.todo_type = todo.todo_type
    else:
        todo.todo_type = todo_type

    if stage is None or not stage:
        todo.stage = todo.stage
    else:
        todo.stage = stage
    
    if acceptance is None or not acceptance:
        todo.acceptance = todo.acceptance
    else:
        todo.acceptance = acceptance
    
    if due_date is None or not due_date:
        todo.due_date = todo.due_date
    else:
        todo.due_date = due_date

    if details is None or not details:
        todo.details = todo.details
    else:
        todo.details = details

    db.session.commit()
    return jsonify(user.serialize())