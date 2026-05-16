from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.repositories.product_repository import ProductRepository
from src.api.v1.schemas.batch import BatchCreate, BatchResponse, BatchListResponse, BatchUpdate, \
    ProductAggregateRequest, ProductAggregateResponse
from src.core.database import get_db
from src.data.repositories.batch_repository import BatchRepository
from src.data.repositories.work_center_repository import WorkCenterRepository
from src.domain.services.batch_service import BatchService

router = APIRouter(prefix="/batches", tags=["Batch"])


def get_batch_service(db: AsyncSession = Depends(get_db)) -> BatchService:
    return BatchService(
        batch_repository=BatchRepository(db),
        work_center_repository=WorkCenterRepository(db),
        product_repository=ProductRepository(db)
    )


@router.post("/{batch_id}/aggregate", response_model=ProductAggregateResponse,
             status_code=status.HTTP_200_OK,
             summary="Агрегировать продукцию в партии",
             description="Агрегировать определенную продукцию по unique_code в партии по ее id", )
async def aggregate_products(batch_id : int,
                             product_to_aggregate : ProductAggregateRequest,
                             batch_service: BatchService = Depends(get_batch_service),
                             ):
    return await batch_service.aggregate_products(batch_id,product_to_aggregate)


@router.post("/", response_model=list[BatchResponse],
             status_code=status.HTTP_201_CREATED,
             summary="Создать партии",
             description="Создать новые партии", )
async def create_batches(
        batches_data: list[BatchCreate],
        batch_service: BatchService = Depends(get_batch_service),
):
    return await batch_service.create_batches(batches_data)


@router.get("/", response_model=BatchListResponse,
            status_code=status.HTTP_200_OK,
            summary="Получить партии",
            description="Получить партии по фильтрам")
async def get_batches(
        is_closed: Optional[bool] = Query(None),
        batch_number: Optional[int] = Query(None, gt=0),
        batch_date: Optional[date] = Query(None),
        work_center_id: Optional[int] = Query(None, gt=0),
        shift: Optional[str] = Query(None),
        offset: int = Query(0, ge=0),
        limit: int = Query(20, ge=1, le=100),
        batch_service: BatchService = Depends(get_batch_service),
):
    return await batch_service.get_batches(
        is_closed=is_closed,
        batch_number=batch_number,
        batch_date=batch_date,
        work_center_id=work_center_id,
        shift=shift,
        offset=offset,
        limit=limit,
    )


@router.get("/{batch_id}", response_model=BatchResponse,
            status_code=status.HTTP_200_OK,
            summary="Получить партию",
            description="Получить партию по id с списком продукции")
async def get_batch(batch_id: int, batch_service: BatchService = Depends(get_batch_service)):
    return await batch_service.get_batch(batch_id)


@router.patch("/{batch_id}", response_model=BatchResponse,
              status_code=status.HTTP_200_OK,
              summary="Изменить партию",
              description="Изменить партию по id")
async def patch_batch(batch_id: int, batch_data: BatchUpdate, batch_service: BatchService = Depends(get_batch_service)):
    return await batch_service.patch_batch(batch_id, batch_data)
