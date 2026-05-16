from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.schemas.batch import BatchCreate, BatchResponse, BatchListResponse, BatchUpdate
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



@router.get("/",response_model=BatchListResponse,
             status_code=status.HTTP_200_OK,
             summary="Получить партии",
             description="Получить партии по фильтрам")
async def get_batches(
    is_closed: Optional[bool] = Query(None),
    batch_number: Optional[int] = Query(None, gt=0),
    batch_date: Optional[date] = Query(None),
    shift: Optional[str] = Query(None),
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    batch_service: BatchService = Depends(get_batch_service),
):
    return await batch_service.get_batches(
        is_closed=is_closed,
        batch_number=batch_number,
        batch_date=batch_date,
        shift=shift,
        offset=offset,
        limit=limit,
    )
@router.get("/{batch_id}",response_model=BatchResponse,
             status_code=status.HTTP_200_OK,
             summary="Получить партию",
             description="Получить партию по id с списком продукции")
async def get_batch(batch_id: int, batch_service: BatchService = Depends(get_batch_service)):
    return await batch_service.get_batch(batch_id)

@router.patch("/{batch_id}", response_model=BatchResponse,
             status_code=status.HTTP_200_OK,
             summary="Изменить партию",
             description="Изменить партию по id")
async def patch_batch(batch_id: int, batch_data : BatchUpdate, batch_service: BatchService = Depends(get_batch_service)):
    return await batch_service.patch_batch(batch_id, batch_data)