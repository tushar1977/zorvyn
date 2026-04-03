from flask_jwt_extended import create_access_token, create_refresh_token
from app.models.user import User
from app.models.role import Role
from app.extensions import db


class AuthService:
    @staticmethod
    def register(data):
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        if not name or not email or not password:
            return None, "name, email, password required"

        if User.query.filter_by(email=email).first():
            return None, "email already exists"

        role = Role.query.filter_by(name="viewer").first()
        if not role:
            return None, "default role not found"

        user = User(
            name=name,
            email=email,
            role_id=role.id,
        )

        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        return user.to_dict(), None

    @staticmethod
    def login(email, password):
        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            return None, "invalid credentials"

        if user.status.value != "active":
            return None, "account inactive"

        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        return {
            "user_id": user.id,
            "role": user.role.name,
            "access_token": access_token,
            "refresh_token": refresh_token,
        }, None

    @staticmethod
    def refresh(user):
        return user.to_dict()

    @staticmethod
    def logout(user):
        return True
