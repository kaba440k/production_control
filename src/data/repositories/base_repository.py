from typing import TypeVar, Generic, Type, Optional, List

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.database import Base

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    """Базовый репозиторий для всех моделей"""

    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session
        self.model = model

    # ====================== Основные CRUD ======================

    async def get(self, id: int) -> Optional[T]:
        """Получить по ID"""
        return await self.session.get(self.model, id)

    async def get_with_relations(self, id: int, *relations) -> Optional[T]:
        """Получить с подгрузкой связанных сущностей (selectinload)"""
        stmt = select(self.model).where(self.model.id == id)
        for relation in relations:
            stmt = stmt.options(selectinload(relation))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, **kwargs) -> T:
        """Создать новую запись"""
        obj = self.model(**kwargs)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, id: int, **kwargs) -> Optional[T]:
        """Обновить запись"""
        stmt = (
            update(self.model)
            .where(self.model.id == id)
            .values(**kwargs)
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one_or_none()

    async def delete(self, id: int) -> bool:
        """Удалить запись"""
        stmt = delete(self.model).where(self.model.id == id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0

    # ====================== Получение списков ======================

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        order_by: str = "created_at",
        desc: bool = True,
        **filters
    ) -> List[T]:
        """Получить список с пагинацией и фильтрами"""
        stmt = select(self.model)

        # Применяем фильтры
        for field, value in filters.items():
            if value is not None and hasattr(self.model, field):
                stmt = stmt.where(getattr(self.model, field) == value)

        # Сортировка
        order_column = getattr(self.model, order_by, self.model.created_at)
        if desc:
            stmt = stmt.order_by(order_column.desc())
        else:
            stmt = stmt.order_by(order_column)

        stmt = stmt.offset(skip).limit(limit)

        result = await self.session.execute(stmt)
        return list(result.scalars().all())