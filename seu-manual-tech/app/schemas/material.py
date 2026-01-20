from app.schemas.core import CamelSchema
from datetime import datetime
from pydantic import Field


class MaterialBase(CamelSchema):
    nome: str = Field(..., min_length=1, max_length=200)
    preco_unitario: float = Field(..., gt=0, description="Preço unitário do material")


class MaterialCreate(MaterialBase):
    pass


class MaterialSchema(MaterialBase):
    id: int
    created_at: datetime | None = None


class MaterialConsumoBase(CamelSchema):
    """Schema para adicionar material a uma manutenção"""
    material_id: int
    quantidade: float = Field(..., gt=0, description="Quantidade do material a ser consumida")


class MaterialConsumoCreate(MaterialConsumoBase):
    pass


class MaterialConsumoSchema(CamelSchema):
    """Schema para exibir material consumido em uma manutenção"""
    id: int
    nome: str
    quantidade: float
    preco_unitario: float
    custo: float = Field(..., description="Custo total = quantidade * preco_unitario")
