from __future__ import annotations
from sqlalchemy import Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.core import BaseColumns


class ManutencaoMaterial(BaseColumns):
    """Tabela de associação para rastrear consumo de materiais em manutenções"""
    __tablename__ = "manutencao_materiais"

    manutencao_id: Mapped[int] = mapped_column(ForeignKey("manutencoes.id"), index=True)
    material_id: Mapped[int] = mapped_column(ForeignKey("materiais.id"), index=True)
    quantidade: Mapped[float] = mapped_column(Numeric(10, 2))
    manutencao: Mapped["Manutencao"] = relationship("Manutencao", back_populates="materiais_consumidos")  
    material: Mapped["Material"] = relationship("Material", back_populates="consumos")
    
    @property
    def custo_calculado(self) -> float:
        return float(self.quantidade) * float(self.material.preco_unitario)