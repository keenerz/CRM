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
    return jsonify({"email": email_get})

@api.route('/user', methods=['POST'])
def create_user():
    email = request.json.get('email')
    password = request.json.get('password')
    usertype = request.json.get('usertype')
    user = User(email=email, password=password, usertype=usertype)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize())

@api.route('/user', methods=['DELETE'])
@jwt_required()
def delete_user():
    email = request.json.get('email')
    password = request.json.get('password')
    usertype = request.json.get('usertype')
    user = User.query.filter_by(email=email, password=password, usertype=usertype).first()
    if user is None: 
        return jsonify({"msg": "Invalid user"}), 400
    db.session.delete(user)
    db.session.commit()
    return jsonify({ "msg": "User Deleted"}), 200

@api.route('/user', methods=['PUT'])
@jwt_required()
def update_user():
    current_user_id = get_jwt_identity()
    user = User.query.filter_by(id=current_user_id).first()
    if user is None:
        return jsonify({"msg":"User doesn't exist"}), 400
    email = request.json.get('email')
    password = request.json.get('password')
    usertype = request.json.get('usertype')

    if email is None or not email:
        user.email = user.email
    else:
        user.email = email

    if password is None or not password:
        user.password = user.password
    else:
        user.password = password
    
    if usertype is None or not usertype:
        user.usertype = user.usertype
    else:
        user.usertype = usertype
 
    db.session.commit()
    return jsonify(user.serialize())


#Todo Endpoints
@api.route('/todos', methods=['GET'])
@jwt_required()
def get_task():
    user_id = get_jwt_identity()
    todos_query = Todos.query.all()
    all_serialized_project = list(map(lambda item:item.serialize(), todos_query))
    return jsonify(all_serialized_project)

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