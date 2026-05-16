from datetime import datetime, date
from typing import Optional, List

from src.core.database import Base
from src.data.models.WorkCenter import WorkCenter
from sqlalchemy import String, Boolean, DateTime, ForeignKey, func, UniqueConstraint, Index, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Batch(Base):
    __tablename__ = "batches"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        index=True
    )
    # Статус
    is_closed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )
    closed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    # Описание задания
    task_description: Mapped[str] = mapped_column(
        String(2000),
        nullable=False
    )
    work_center_id: Mapped[int] = mapped_column(
        ForeignKey("work_centers.id", ondelete="RESTRICT"),
        nullable=False
    )
    shift: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )
    team: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    # Идентификация партии
    batch_number: Mapped[int] = mapped_column(
        nullable=False,
        index=True
    )
    batch_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True
    )

    # Продукция
    nomenclature: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )
    ekn_code: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    # Временные рамки
    shift_start: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )
    shift_end: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    # Метаданные
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

    products: Mapped[List["Product"]] = relationship(
        "Product",
        back_populates="batch",
        cascade="all, delete-orphan"
    )

    work_center: Mapped["WorkCenter"] = relationship(
        "WorkCenter",
        back_populates="batches"
    )

    # ==================== Индексы и ограничения ====================
    __table_args__ = (
        # Уникальность: нельзя создать две одинаковые партии (номер + дата)
        UniqueConstraint("batch_number", "batch_date", name="uq_batch_number_date"),

        # Индексы для частых запросов
        Index("idx_batch_closed", "is_closed"),
        Index("idx_batch_shift_times", "shift_start", "shift_end"),
    )

    def __repr__(self) -> str:
        return f"<Batch #{self.batch_number} ({self.batch_date}), task_description = {self.task_description}>"
