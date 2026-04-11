from datetime import datetime
from typing import List, Optional

from src.core.database import Base

from sqlalchemy import String, Boolean, DateTime, ForeignKey, func, ARRAY, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship


class WebhookSubscription(Base):
    __tablename__ = "webhook_subscriptions"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        index=True
    )
    url: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )
    events: Mapped[List[str]] = mapped_column(
        ARRAY(String),
        nullable=False
    )
    secret_key: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )
    retry_count: Mapped[int] = mapped_column(
        Integer,
        default=3,
        nullable=False
    )
    timeout: Mapped[int] = mapped_column(
        Integer,
        default=10,
        nullable=False
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

    webhook_deliveries: Mapped[List["WebhookDelivery"]] = relationship(
        "WebhookDelivery",
        back_populates="subscription",
        cascade="all, delete-orphan"
    )


class WebhookDelivery(Base):
    __tablename__ = "webhook_deliveries"
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        index=True
    )
    subscription_id: Mapped[int] = mapped_column(
        ForeignKey("webhook_subscriptions.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    event_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    payload: Mapped[dict] = mapped_column(
        JSON,
        nullable=False
    )
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        index=True
    )  # pending, success, failed

    attempts: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    response_status: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    response_body: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)

    error_message: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    delivered_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    subscription: Mapped["WebhookSubscription"] = relationship(
        "WebhookSubscription",
        back_populates="webhook_deliveries"
    )
