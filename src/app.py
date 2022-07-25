from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

from api.v1.resourses.auth import auth
from api.v1.resourses.roles import roles
from api.v1.resourses.users import users

from db.db import init_db

app = Flask(__name__)

jwt = JWTManager(app)
db = SQLAlchemy(app)

app.register_blueprint(auth, url_prefix='/api/v1/auth')
app.register_blueprint(roles, url_prefix='/api/v1/roles')
app.register_blueprint(users, url_prefix='/api/v1/users')

def main():
    init_db(app)
    app.run()


if __name__ == '__main__':
    main()
