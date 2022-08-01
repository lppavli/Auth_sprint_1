import os
import time

import pytest
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from flask import jsonify, url_for
from flask_jwt_extended import create_access_token, create_refresh_token
from sqlalchemy import delete

from models.db_models import UserRole

BASE_DIR = os.path.abspath(os.path.join(__file__, "../../../"))
# https://github.com/serlesen/backend-flask/blob/chapter_5/tests/conftest.py
from src import create_app
from db.db import db
from models import User, Role


@pytest.fixture(scope="session")
def flask_app():
    app = create_app()
    client = app.test_client()
    ctx = app.test_request_context()
    ctx.push()

    yield client

    ctx.pop()


@pytest.fixture(scope="session")
def app_with_db(flask_app):
    db.create_all()

    yield flask_app

    db.session.commit()
    db.drop_all()


@pytest.fixture(scope="function")
def user(app_with_db):
    user = User()
    user.login = "sergio"
    user.set_password("pass")
    db.session.add(user)
    db.session.commit()

    yield user

    db.session.execute(delete(User))
    db.session.commit()


@pytest.fixture()
def access_token(user):
    return {"Authorization": f"Bearer {create_access_token(identity=user.id).decode('utf-8')}"}


@pytest.fixture()
async def refresh_token(user) -> dict:
    return {"Authorization": f"Bearer {create_refresh_token(identity=user.id).decode('utf-8')}"}


@pytest.fixture(scope="function")
def login_super_user(app_with_db):
    user = User(is_superuser=True)
    user.login = "admin"
    user.set_password("admin")
    db.session.add(user)
    db.session.commit()
    admin_role = Role(name="admin")
    db.session.add(admin_role)
    db.session.commit()
    access_token = create_access_token(identity=user.id,
                                       additional_claims={"is_administrator": True}).decode('utf-8')
    new_role_user = UserRole(user_id=user.id, role_id=admin_role.id)
    db.session.add(new_role_user)
    db.session.commit()

    yield {"Authorization": f"Bearer {access_token}"}

    db.session.execute(delete(User))
    db.session.execute(delete(Role))
    db.session.execute(delete(UserRole))
    db.session.commit()


@pytest.fixture()
def create_role(login_super_user):
    role = Role(name="user")
    db.session.add(role)
    db.session.commit()

    yield role.id

    db.session.execute(delete(Role))
    db.session.commit()
