import uuid
from datetime import datetime
from typing import List
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from src.core.database import Base

class WorkCenter(Base):
    __tablename__ = "work_centers"

    """Уникальный ID. Генерируется автоматически."""
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)

    identifier : Mapped[str] = mapped_column(
        String(50),
        unique = True,
        nullable = False,
        index = True
    )
    name : Mapped[str] = mapped_column(
        String(200),
        nullable = False
    )
    """Дата создания. Автоматически устанавливается БД при INSERT."""
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    """Дата обновления. Автоматически обновляется БД при UPDATE."""
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    batches : Mapped[List["Batch"]] = relationship(
        "Batch",
        back_populates="work_center",
        cascade = "all, delete-orphan"
    )
    def __repr__(self) -> str:
        return f"<WorkCenter(id={self.id}), name = {self.name}>"

