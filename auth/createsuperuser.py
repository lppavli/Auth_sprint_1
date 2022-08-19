from app import create_app
from db.db import db
from models import User, Role
from models.db_models import UserRole


def createsuperuser(login="admin", password="admin"):
    user_exist = db.session.query(User).filter(User.login == login).first()
    if user_exist:
        return "User already exist. Try another login"
    superuser = User(login=login, is_superuser=True)
    superuser.set_password(password)
    db.session.add(superuser)
    db.session.commit()
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()
    new_role_user = UserRole(user_id=superuser.id, role_id=role.id)
    db.session.add(new_role_user)
    db.session.commit()
    return "Superuser login=admin, password=admin was created"


if __name__ == "__main__":
    db.create_all(app=create_app())
    print(createsuperuser("admin", "admin"))
