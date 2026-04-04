import uuid
from sqlalchemy.sql.sqltypes import UUID
from sqlalchemy.types import String
from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Role(db.Model):
    __tablename__ = "roles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str]
    users: Mapped[list["User"]] = relationship("User", back_populates="role")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }
