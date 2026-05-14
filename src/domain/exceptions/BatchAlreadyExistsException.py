from datetime import date

from src.core.exceptions import AppException


class BatchAlreadyExistsException(AppException):
    """Партия с таким номером и датой уже существует."""
    def __init__(self, batch_number: int, batch_date : date):
        super().__init__(
            message=f"Batch with number '{batch_number}' and date '{batch_date}' already exists",
            status_code=409,
        )