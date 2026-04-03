from typing import List

from sqlalchemy import Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.utils.enums import CategoryType
from app.extensions import db


class Category(db.Model):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    type: Mapped[CategoryType] = mapped_column(
        Enum(CategoryType, name="category_type"), nullable=False
    )

    records: Mapped[List["FinancialRecord"]] = relationship(
        "FinancialRecord", back_populates="category"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type.value,
        }
