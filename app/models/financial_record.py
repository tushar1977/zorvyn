from sqlalchemy import (
    Integer,
    DateTime,
    Date,
    Numeric,
    Boolean,
    ForeignKey,
    Text,
    Enum,
)
from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from typing import Optional
from decimal import Decimal


from app.utils.enums import RecordType


class FinancialRecord(db.Model):
    __tablename__ = "financial_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"), nullable=False
    )

    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)

    type: Mapped[RecordType] = mapped_column(
        Enum(RecordType, name="record_type"), nullable=False
    )

    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    record_date: Mapped[datetime] = mapped_column(Date, nullable=False)

    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

    user: Mapped["User"] = relationship("User", back_populates="records")
    category: Mapped["Category"] = relationship("Category", back_populates="records")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "category": self.category.name if self.category else None,
            "amount": float(self.amount),
            "type": self.type.value,
            "notes": self.notes,
            "record_date": self.record_date.isoformat(),
            "created_at": self.created_at.isoformat(),
        }
