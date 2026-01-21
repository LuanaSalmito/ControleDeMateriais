from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import String, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.core import BaseColumns

if TYPE_CHECKING:
    from app.models.manutencao_material import ManutencaoMaterial


class Material(BaseColumns):
    """Catálogo de materiais disponíveis para uso em manutenções"""
    __tablename__ = "materiais"

    nome: Mapped[str] = mapped_column(String(200), unique=True, index=True)
    preco_unitario: Mapped[float] = mapped_column(Numeric(10, 2))
    
    
    consumos: Mapped[list["ManutencaoMaterial"]] = relationship(
        "ManutencaoMaterial", back_populates="material"
    )
