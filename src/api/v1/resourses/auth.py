from datetime import timedelta
from http import HTTPStatus
from flask_pydantic import validate
import click
import redis
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt, get_jwt_identity
from werkzeug.security import generate_password_hash

from db.db import db
from models import User
from models.db_models import UserHistory
from api.v1.schemas.users import UserCreate, UserLogin, History, PasswordChange

auth = Blueprint('auth', __name__)
admin_create = Blueprint('admin', __name__, cli_group=None)

jwt_redis_blocklist = redis.StrictRedis(host="localhost",  # os.getenv("REDIS_HOST"),
                                        port=6379,  # os.getenv("REDIS_PORT"),
                                        db=0, decode_responses=True)


@admin_create.cli.command("createsuperuser")
@click.argument('name')
@click.argument('password')
def create_superuser(login, password):
    user_exist = db.session.query(User).filter(User.login == login).first()
    if user_exist:
        return "User already exist. Try another login"
    superuser = User(login=login, is_superuser=True)
    superuser.set_password(password)
    db.session.add(superuser)
    db.session.commit()
    return "Superuser created"


@auth.route("/signup", methods=["POST"])
def create_user():
    user = UserCreate(**request.get_json())
    user_exist = db.session.query(User).filter(User.login == user.login).first()
    if user_exist:
        return {"msg": "User already exist"}, HTTPStatus.CONFLICT
    new_user = User(login=user.login)
    new_user.set_password(user.password)
    db.session.add(new_user)
    db.session.commit()
    return {"msg": "User was created."}, HTTPStatus.CREATED


@auth.route('/login', methods=['POST'])
@validate()
def login_user(body: UserLogin):
    # data = UserLogin(**request.get_json())
    user = db.session.query(User).filter(User.login == body.login).first()
    if not user:
        return {"msg": "User is not found"}, HTTPStatus.NOT_FOUND
    user_id = str(user.id)
    user_agent = request.headers.get('user-agent', '')
    user_host = request.headers.get('host', '')
    user_info = UserHistory(user_id=user_id,
                            user_agent=user_agent,
                            ip_address=user_host,
                            )
    if user.check_password(body.password):

        if user.is_superuser:
            access_token = create_access_token(identity=user.id,
                                               additional_claims={"is_administrator": True})
            refresh_token = create_refresh_token(identity=user.id)

        else:
            access_token = create_access_token(identity=user.id,
                                               additional_claims={"is_administrator": False})
            refresh_token = create_refresh_token(identity=user.id)

        db.session.add(user_info)
        db.session.commit()
        db.session.remove()
        return {"message": "Successful Entry",
                "user": user_id,
                "access_token": str(access_token),
                "refresh_token": str(refresh_token)}
    return jsonify({'message': 'Wrong password'})


@auth.route('/logout', methods=['DELETE'])
@jwt_required()
def logout():
    jti = get_jwt()['jti']
    jwt_redis_blocklist.set(jti, "", ex=timedelta(minutes=5))
    return {"msg": "Access token revoked"}


@auth.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return {"access_token": str(access_token)}


@auth.route('/change-password', methods=['PATCH'])
@validate()
@jwt_required()
def change_password(body: PasswordChange):
    identity = get_jwt_identity()
    user = User.query.filter_by(id=identity).first()
    print(user.id, user.login, user.password)
    print(type(user))
    if user is None:
        return {'message': 'User not found. Check uuid'}

    if user.check_password(body.old_password):
        new_password = generate_password_hash(body.new_password)
        db.session.query(User).filter_by(id=user.id).update({'password': new_password})
        db.session.commit()
        return {'message': 'Password changed successfully'}

    return {'message': 'You entered the wrong old password'}


@auth.route('/history', methods=['GET'])
@jwt_required()
@validate(response_many=True)
def get_history():
    page = request.args.get("page", default=1, type=int)
    page_size = request.args.get("page_size", default=10, type=int)
    identity = get_jwt_identity()
    history = UserHistory.query.filter_by(user_id=identity).paginate(
        page, per_page=page_size
    )
    return [History(user_agent=row.user_agent, ip_address=row.ip_address, auth_datetime=row.auth_datetime)
            for row in history.items]
