from datetime import date

from src.core.exceptions import NotFoundException


class BatchNotFoundException(NotFoundException):
    """Партия с таким id не найдена"""
    def __init__(self, batch_id: int):
        super().__init__(resource="Batch", identifier=batch_id)