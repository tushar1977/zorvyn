from app.models.user import User
from app.models.role import Role
from app.extensions import db
from app.utils.enums import UserStatus


class UserService:
    @staticmethod
    def create_user(data):
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        role_name = data.get("role")

        if not name or not email or not password:
            return None, "name, email, password required"

        if User.query.filter_by(email=email).first():
            return None, "email already exists"

        if role_name:
            role = Role.query.filter_by(name=role_name).first()
            if not role:
                return None, "invalid role"
        else:
            role = Role.query.filter_by(name="viewer").first()

        user = User(
            name=name,
            email=email,
            role_id=role.id,
        )

        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        return user, None

    @staticmethod
    def get_all_users():
        return User.query

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.filter_by(id=user_id).first()

    @staticmethod
    def update_user(user, data):
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        if email:
            existing = User.query.filter_by(email=email).first()
            if existing and existing.id != user.id:
                return None, "email already in use"

        if name:
            user.name = name
        if email:
            user.email = email
        if password:
            user.set_password(password)

        db.session.commit()

        return user, None

    @staticmethod
    def update_status(user, status):
        if status not in ["active", "inactive"]:
            return None, "invalid status"

        user.status = UserStatus.ACTIVE if status == "active" else UserStatus.INACTIVE

        db.session.commit()
        return user, None
