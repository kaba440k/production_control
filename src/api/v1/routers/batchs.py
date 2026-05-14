from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.schemas.batch import BatchCreate, BatchResponse
from src.core.database import get_db
from src.data.repositories.batch_repository import BatchRepository
from src.data.repositories.work_center_repository import WorkCenterRepository
from src.domain.services.batch_service import BatchService

router = APIRouter(prefix="/batchs", tags=["Batch"])


def get_batch_service(db: AsyncSession = Depends(get_db)) -> BatchService:
    return BatchService(
        batch_repository=BatchRepository(db),
        work_center_repository=WorkCenterRepository(db),
    )


@router.post("/", response_model=BatchResponse,
             status_code=status.HTTP_201_CREATED,
             summary="Создать партию",
             description="Создать новую партию с списком продукции", )
async def create_batch(
        batch_data: BatchCreate,
        batch_service: BatchService = Depends(get_batch_service),
):

    return await batch_service.create_batch(batch_data)
