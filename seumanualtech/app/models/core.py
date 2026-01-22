from datetime import datetime
from sqlalchemy import DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.database.core import Base


class BaseColumns(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    flag_ativo: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true")

    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    atualizado_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())
