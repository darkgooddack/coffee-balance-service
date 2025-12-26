import datetime
import uuid
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column

from app.database.db import Base


class Balance(Base):
    __tablename__ = "users"

    user_id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True
    )
    balance: Mapped[int] = mapped_column(
        nullable=False,
        default=0
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now()
    )
