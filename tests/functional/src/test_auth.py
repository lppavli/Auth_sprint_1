from flask import url_for, request
from flask_jwt_extended import create_access_token

from db.db import db
from models import User
from models.db_models import UserHistory
from http import HTTPStatus


def test_auth_user(app_with_db, user):
    response = app_with_db.post(
        url_for("auth.login_user"),
        json={
            "login": "sergio",
            "password": "pass"
        }
    )
    assert response.status_code == HTTPStatus.OK


def test_auth_unknown_user(app_with_db, user):
    response = app_with_db.post(
        url_for("auth.login_user"),
        json={
            "login": "joe",
            "password": "pass"
        }
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_create_user(app_with_db):
    response = app_with_db.post(url_for("auth.create_user"),
                                json={
                                    "login": "John",
                                    "password": "Abcdefgh"
                                })
    assert response.status_code == HTTPStatus.CREATED
    assert response.json['msg'] == "User was created."


def test_get_user_history(app_with_db, user, access_token):
    user_id = str(user.id)
    user_agent = request.headers.get('user-agent', '')
    user_host = request.headers.get('host', '')
    user_info = UserHistory(user_id=user_id,
                            user_agent=user_agent,
                            ip_address=user_host,
                            )
    response = app_with_db.get(url_for("auth.get_history"),
                               headers=access_token
                               )
    assert response.status_code == HTTPStatus.OK


def test_logout(app_with_db, access_token):
    response = app_with_db.delete(
        url_for("auth.logout"),
        headers=access_token
    )
    assert response.status == "200 OK"
    assert response.json['msg'] == 'Access token revoked'