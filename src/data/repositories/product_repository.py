from typing import Optional, List

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.models.Product import Product
from src.data.repositories.base_repository import BaseRepository


class ProductRepository(BaseRepository[Product]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Product)

    async def get_by_unique_code(self, unique_code: str) -> Optional[Product]:
        """Найти продукт по его уникальному коду (unique_code)"""
        stmt = select(self.model).where(self.model.unique_code == unique_code)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_batch_id(self, batch_id: int, is_aggregated: bool | None = None) -> List[Product]:
        """Получить все продукты конкретной партии
            Если передан is_aggregated, то фильтровать по статусу агрегации"""
        stmt = select(self.model).where(self.model.batch_id == batch_id)
        if is_aggregated is not None:
            stmt = stmt.where(self.model.is_aggregated == is_aggregated)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def count_by_batch(self, batch_id: int) -> int:
        """Посчитать общее количество продуктов в партии"""
        stmt = select(func.count()).select_from(self.model).where(
            self.model.batch_id == batch_id
        )
        result = await self.session.execute(stmt)
        return result.scalar() or 0
