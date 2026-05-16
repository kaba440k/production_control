from src.domain.exceptions.BatchNotFoundException import BatchNotFoundException
from src.domain.exceptions.ProductAlreadyExistsException import ProductAlreadyExistsException
from src.api.v1.schemas.product import ProductCreate
from src.data.repositories.batch_repository import BatchRepository
from src.data.repositories.product_repository import ProductRepository
from src.data.models.Product import Product


class ProductService:
    def __init__(self, product_repository : ProductRepository, batch_repository : BatchRepository):
        self.product_repo = product_repository
        self.batch_repo = batch_repository


    async def create_product(self, product_data: ProductCreate) -> Product | None:
        existing_batch = await self.batch_repo.get(product_data.batch_id)
        if existing_batch is None:
            raise BatchNotFoundException(product_data.batch_id)

        existing_product = await self.product_repo.get_by_unique_code(product_data.unique_code)
        if existing_product is not None:
            raise ProductAlreadyExistsException(product_data.unique_code)
        created_product = await self.product_repo.create(
            batch_id = product_data.batch_id,
            unique_code = product_data.unique_code
        )
        return created_product