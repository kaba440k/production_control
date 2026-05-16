from src.core.exceptions import NotFoundException


class ProductNotFoundException(NotFoundException):
    """Продукция с таким id не найдена"""
    def __init__(self, product_id: int):
        super().__init__(resource="Product", identifier=product_id)