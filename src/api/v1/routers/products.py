from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.schemas.product import ProductResponse, ProductCreate
from src.core.database import get_db
from src.data.repositories.batch_repository import BatchRepository
from src.data.repositories.product_repository import ProductRepository
from src.domain.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["Product"])


def get_product_service(db: AsyncSession = Depends(get_db)) -> ProductService:
    return ProductService(
        product_repository=ProductRepository(db),
        batch_repository=BatchRepository(db),
    )


@router.post("/", response_model=ProductResponse,
             status_code=status.HTTP_201_CREATED,
             summary="Создать продукцию",
             description="Создать новую продукцию для конкретной партии", )
async def create_product(product_data: ProductCreate, product_service: ProductService= Depends(get_product_service)):
    return await product_service.create_product(product_data)
