import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class DisabilityType(str, enum.Enum):
    visual = "visual"
    developmental = "developmental"
    hearing = "hearing"
    none = "none"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    nickname: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    disability_type: Mapped[DisabilityType] = mapped_column(
        Enum(DisabilityType), nullable=False, default=DisabilityType.none
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
