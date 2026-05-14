from datetime import date
from os.path import exists
from typing import Optional

from sqlalchemy import select, exists, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

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

    async def get_filtered(
            self,
            is_closed: Optional[bool] = None,
            batch_number: Optional[int] = None,
            batch_date: Optional[date] = None,
            shift: Optional[str] = None,
            offset: int = 0,
            limit: int = 20,
    ) -> tuple[list[Batch], int]:
        stmt = select(self.model).options(selectinload(self.model.products))

        count_stmt = select(func.count()).select_from(self.model)

        filters = []

        if is_closed is not None:
            filters.append(self.model.is_closed == is_closed)

        if batch_number is not None:
            filters.append(self.model.batch_number == batch_number)

        if batch_date is not None:
            filters.append(self.model.batch_date == batch_date)

        if shift is not None:
            filters.append(self.model.shift == shift)

        if filters:
            stmt = stmt.where(*filters)
            count_stmt = count_stmt.where(*filters)

        stmt = stmt.order_by(self.model.created_at.desc()).offset(offset).limit(limit)

        items_result = await self.session.execute(stmt)
        total_result = await self.session.execute(count_stmt)

        return list(items_result.scalars().all()), total_result.scalar() or 0