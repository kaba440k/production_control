from src.core.exceptions import AppException


class ProductAlreadyExistsException(AppException):
    """Продукция с таким номером и датой уже существует."""
    def __init__(self, unique_code : str):
        super().__init__(
            message=f"Product with unique_code {unique_code} already exists",
            status_code=409,
        )