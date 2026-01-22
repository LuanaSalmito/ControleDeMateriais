from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import String, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.core import BaseColumns
from app.models.enums import StatusManutencao

if TYPE_CHECKING:
    from app.models.manutencao_material import ManutencaoMaterial


class Manutencao(BaseColumns):
    __tablename__ = "manutencoes"

    resumo: Mapped[str] = mapped_column(String(500))
    status: Mapped[StatusManutencao] = mapped_column(
        SQLEnum(StatusManutencao, native_enum=False, length=50),
        default=StatusManutencao.ABERTO,
        nullable=False
    )
    
    materiais_consumidos: Mapped[list["ManutencaoMaterial"]] = relationship( 
                                                                            
        "ManutencaoMaterial", back_populates="manutencao", lazy="selectin"
    )
    
    @property
    def custo_total_materiais(self) -> float:
        """
        Calcula o custo total de todos os materiais consumidos nesta manutenção.
        
        Returns:
            Soma dos custos de todos os materiais consumidos
        """
        return sum(consumo.custo_calculado for consumo in self.materiais_consumidos)