import datetime
import uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.database.db import Base


class BalanceModel(Base):
    __tablename__ = "balance"

    user_id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    balance: Mapped[int] = mapped_column(nullable=False, default=0)
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
