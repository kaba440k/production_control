from datetime import date
from os.path import exists
from typing import Optional

from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession


from src.data.models.Batch import Batch
from src.data.repositories.base_repository import BaseRepository


class BatchRepository(BaseRepository[Batch]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Batch)

    async def get_with_products(self, batch_id: int) -> Optional[Batch]:
        """Получить партию вместе со всеми продуктами"""
        return await super().get_with_relations(batch_id, Batch.products)

    async def get_by_batch_number_and_date(self, batch_number: int, batch_date: date) -> Optional[Batch] :
        stmt = select(self.model).where(self.model.batch_number == batch_number, self.model.batch_date == batch_date)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def exists_by_batch_number_and_date(self, batch_number: int, batch_date: date) -> bool:
        stmt = select(
            exists().where(
                self.model.batch_number == batch_number,
                self.model.batch_date == batch_date
            )
        )

        result = await self.session.execute(stmt)
        return result.scalar() is True