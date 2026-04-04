from flask_jwt_extended import create_access_token, create_refresh_token
from app.models.user import User
from app.models.role import Role
from app.extensions import db
from app.utils.validator import validate_email, validate_required_fields


class AuthService:
    @staticmethod
    def register(data):
        try:
            validate_required_fields(data, ["name", "email", "password"])
            validate_email(data.get("email"))
        except ValueError as e:
            return None, str(e)
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        if User.query.filter_by(email=email).first():
            return None, "email already exists"

        role = Role.query.filter_by(name="viewer").first()
        if not role:
            return None, "default role not found. Consider adding a default role"

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
        try:
            validate_email(email)
        except ValueError as e:
            return None, str(e)
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

    # Currently dummy routes
    @staticmethod
    def refresh(user):
        return user.to_dict()

    @staticmethod
    def logout(user):
        return True
