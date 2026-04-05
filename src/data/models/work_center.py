class WorkCenter(Base):
    __tablename__ = "work_centers"

    id: int (PK, автоинкремент)
    identifier: str (unique, not null, indexed) # ИдентификаторРЦ
    name: str (not null) # Название рабочего центра
    created_at: datetime
    updated_at: datetime