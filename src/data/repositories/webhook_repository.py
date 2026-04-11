# src/data/repositories/webhook_repository.py
from typing import List, Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import JSON

from src.data.models.Webhook import WebhookSubscription
from src.data.models.Webhook import WebhookDelivery
from src.data.repositories.base_repository import BaseRepository


class WebhookRepository(BaseRepository[WebhookSubscription]):
    """
    Репозиторий для работы с вебхуками.
    Работает с двумя моделями: WebhookSubscription и WebhookDelivery.
    """

    def __init__(self, session: AsyncSession):
        # Базовый класс инициализируется с WebhookSubscription (основная модель)
        super().__init__(session, WebhookSubscription)

    # ====================== WebhookSubscription ======================

    async def get_active_subscriptions_for_event(self, event_type: str) -> List[WebhookSubscription]:
        """
        Получить все активные подписки, которые хотят получать указанное событие.
        Это самый важный метод для отправки вебхуков.
        """
        stmt = select(self.model).where(
            self.model.is_active == True,
            self.model.events.contains([event_type])  # проверка, что event_type есть в массиве
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_active_subscriptions(self) -> List[WebhookSubscription]:
        """Получить все активные подписки"""
        stmt = select(self.model).where(self.model.is_active == True)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    # ====================== WebhookDelivery ======================

    async def create_delivery(
            self,
            subscription_id: int,
            event_type: str,
            payload: dict
    ) -> WebhookDelivery:
        """Создать запись о доставке вебхука (pending)"""
        delivery = WebhookDelivery(
            subscription_id=subscription_id,
            event_type=event_type,
            payload=payload,
            status="pending",
            attempts=0
        )
        self.session.add(delivery)
        await self.session.commit()
        await self.session.refresh(delivery)
        return delivery

    async def get_pending_deliveries(self, limit: int = 50) -> List[WebhookDelivery]:
        """Получить доставки, которые нужно отправить (для retry)"""
        stmt = select(WebhookDelivery).where(
            WebhookDelivery.status == "pending"
        ).limit(limit)

        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def mark_as_success(
            self,
            delivery_id: int,
            response_status: int,
            response_body: Optional[str] = None
    ) -> Optional[WebhookDelivery]:
        """Отметить доставку как успешную"""
        stmt = select(WebhookDelivery).where(WebhookDelivery.id == delivery_id)
        result = await self.session.execute(stmt)
        delivery = result.scalar_one_or_none()

        if delivery:
            delivery.status = "success"
            delivery.response_status = response_status
            delivery.response_body = response_body
            delivery.delivered_at = func.now()
            await self.session.commit()
            await self.session.refresh(delivery)

        return delivery