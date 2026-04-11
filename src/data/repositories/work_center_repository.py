from typing import Optional


from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.models.WorkCenter import WorkCenter
from src.data.repositories.base_repository import BaseRepository


class WorkCenterRepository(BaseRepository[WorkCenter]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, WorkCenter)

    async def get_by_identifier(self, identifier: str) -> Optional[WorkCenter]:
        """Получить рабочий центр по уникальному идентификатору (RC-001 и т.п.)"""
        stmt = select(self.model).where(self.model.identifier == identifier).limit(1)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()