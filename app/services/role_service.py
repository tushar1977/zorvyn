from app.models.role import Role
from app.extensions import db


class RoleService:
    @staticmethod
    def get_all_roles():
        return Role.query.all()

    @staticmethod
    def assign_role(user, role_name):
        role = Role.query.filter_by(name=role_name).first()

        if not role:
            return None, "role not found"

        user.role_id = role.id
        db.session.commit()

        return user, None

    @staticmethod
    def seed_roles():
        try:
            roles = ["admin", "analyst", "viewer"]
            created = []

            for r in roles:
                existing = Role.query.filter_by(name=r).first()

                if not existing:
                    role = Role(name=r, description="test desc")
                    db.session.add(role)
                    created.append(r)

            db.session.commit()

            return {"created": created, "message": "roles seeded successfully"}, None

        except Exception as e:
            db.session.rollback()
            return None, str(e)
