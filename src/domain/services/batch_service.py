from datetime import datetime, timezone

from src.data.models.WorkCenter import WorkCenter
from src.data.models.Batch import Batch
from src.api.v1.schemas.batch import BatchCreate
from src.domain.exceptions.BatchAlreadyExistsException import BatchAlreadyExistsException
from src.data.repositories.batch_repository import BatchRepository
from src.data.repositories.work_center_repository import WorkCenterRepository



class BatchService:
    def __init__(self, batch_repository : BatchRepository, work_center_repository: WorkCenterRepository):
        self.batch_repo = batch_repository
        self.work_center_repo = work_center_repository


    async def create_batch(self, batch_data : BatchCreate) -> Batch | None:
    #     1. Проверить, нет ли партии с таким номером и датой.
        existing = await self.batch_repo.get_by_batch_number_and_date(batch_data.batch_number, batch_data.batch_date)
        if existing:
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

    # def _validate_batch_data(data : BatchCreate) -> None:
    #
    # def _validate_
