from __future__ import annotations
from sqlalchemy import String, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.core import BaseColumns


class Material(BaseColumns):
    """Catálogo de materiais disponíveis para uso em manutenções"""
    __tablename__ = "materiais"

    nome: Mapped[str] = mapped_column(String(200), unique=True, index=True)
    preco_unitario: Mapped[float] = mapped_column(Numeric(10, 2))
    
    # Relacionamento com consumos de material
    consumos: Mapped[list["ManutencaoMaterial"]] = relationship(
        "ManutencaoMaterial", back_populates="material"
    )


class ManutencaoMaterial(BaseColumns):
    """Tabela de associação para rastrear consumo de materiais em manutenções"""
    __tablename__ = "manutencao_materiais"

    manutencao_id: Mapped[int] = mapped_column(ForeignKey("manutencoes.id"), index=True)
    material_id: Mapped[int] = mapped_column(ForeignKey("materiais.id"), index=True)
    quantidade: Mapped[float] = mapped_column(Numeric(10, 2))

    # Relacionamentos
    manutencao: Mapped["Manutencao"] = relationship("Manutencao", back_populates="materiais_consumidos")  # type: ignore
    material: Mapped["Material"] = relationship("Material", back_populates="consumos")
