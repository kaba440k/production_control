from datetime import datetime, timezone, date
from typing import Optional


from src.domain.exceptions.BatchNotFoundException import BatchNotFoundException
from src.data.models.WorkCenter import WorkCenter
from src.data.models.Batch import Batch
from src.api.v1.schemas.batch import BatchCreate, BatchListResponse, BatchResponse,BatchUpdate
from src.domain.exceptions.BatchAlreadyExistsException import BatchAlreadyExistsException
from src.data.repositories.batch_repository import BatchRepository
from src.data.repositories.work_center_repository import WorkCenterRepository


class BatchService:
    def __init__(self, batch_repository : BatchRepository, work_center_repository: WorkCenterRepository):
        self.batch_repo = batch_repository
        self.work_center_repo = work_center_repository


    async def create_batch(self, batch_data : BatchCreate) -> Batch | None:
    #     1. Проверить, нет ли партии с таким номером и датой.
        if await self.batch_repo.exists_by_batch_number_and_date(batch_data.batch_number, batch_data.batch_date):
            raise BatchAlreadyExistsException(batch_data.batch_number, batch_data.batch_date)

    # 2. Найти WorkCenter по ИдентификаторРЦ.
        work_center : WorkCenter | None = await self.work_center_repo.get_by_identifier(batch_data.work_center_identifier)

        if work_center is None:
            work_center = await self.work_center_repo.create(
                identifier=batch_data.work_center_identifier,
                name=batch_data.work_center_name,
            )

        created_batch = await self.batch_repo.create(
            is_closed=batch_data.is_closed,
            closed_at=datetime.now(timezone.utc) if batch_data.is_closed else None,
            task_description=batch_data.task_description,
            work_center_id=work_center.id,
            shift=batch_data.shift,
            team=batch_data.team,
            batch_number=batch_data.batch_number,
            batch_date=batch_data.batch_date,
            nomenclature=batch_data.nomenclature,
            ekn_code=batch_data.ekn_code,
            shift_start=batch_data.shift_start,
            shift_end=batch_data.shift_end,
        )

        return await self.batch_repo.get_with_products(created_batch.id)

    async def get_batch(self, batch_id : int) -> Batch | None:
        existed_batch = await self.batch_repo.get_with_products(batch_id)
        if existed_batch is None:
            raise BatchNotFoundException(batch_id)
        return existed_batch

    async def patch_batch(self, batch_id : int, batch_data : BatchUpdate) -> Batch | None:
        existed_batch = await self.batch_repo.get_with_products(batch_id)
        if existed_batch is None:
            raise BatchNotFoundException(batch_id)

        update_fields = batch_data.model_dump(exclude_unset=True)
        if "is_closed" in update_fields:
            if update_fields["is_closed"] is True:
                update_fields["closed_at"] = datetime.now(timezone.utc)

            if update_fields["is_closed"] is False:
                update_fields["closed_at"] = None
        await self.batch_repo.update(batch_id, **update_fields)
        return await self.batch_repo.get_with_products(batch_id)

    async def get_batches(
            self,
            is_closed: Optional[bool] = None,
            batch_number: Optional[int] = None,
            batch_date: Optional[date] = None,
            shift: Optional[str] = None,
            offset: int = 0,
            limit: int = 20,
    ) -> BatchListResponse:
        items, total = await self.batch_repo.get_filtered(
            is_closed=is_closed,
            batch_number=batch_number,
            batch_date=batch_date,
            shift=shift,
            offset=offset,
            limit=limit,
        )
        return BatchListResponse(
            items=[BatchResponse.model_validate(item) for item in items],
            total=total,
            skip=offset,
            limit=limit,
        )
