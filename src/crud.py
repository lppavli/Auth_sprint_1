from flask import jsonify, request
from src.app import app
from src.db import db
from src.models.db_models import User

@app.route('/hello-world')
def hello_world():
    return 'Hello, World!'


@app.route('/user', methods=['GET'])
def get_all_users():
    users = User.query.all()
    output = []
    for user in users:
        user_data = {}
        user_data['id'] = user.id
        user_data['login'] = user.login
        user_data['password'] = user.password
        output.append(user_data)
    return jsonify({'users': output})


@app.route('/user/<user_id>', methods=['GET'])
def get_one_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'message': 'No user found'})
    user_data = {}
    user_data['id'] = user.id
    user_data['login'] = user.login
    user_data['password'] = user.password
    return jsonify({'user': user_data})


@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(**data)
    db.session.add(new_user)
    db.session.commit()
    token = new_user.get_token()
    return jsonify({'message': 'New user created', 'token': token})


@app.route('/user/<user_id>', methods=['PUT'])
def promote_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'message': 'No user found'})
    db.session.commit()
    return jsonify({'message': 'The user has been promoted'})


@app.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'message': 'No user found'})
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'The user has been deleted'})


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.authenticate(**data)
    token = user.get_token()
    return jsonify({'message': 'New user created', 'token': token})
    if not user:
        return make_response("could not verify", 401, {"WWW-Authenticate": 'Basic realm="Login required'})
