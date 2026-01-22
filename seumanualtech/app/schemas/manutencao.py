from app.schemas.core import CamelSchema
from app.schemas.material import MaterialConsumoSchema
from app.models.enums import StatusManutencao
from datetime import datetime


class ManutencaoBase(CamelSchema):
    resumo: str
    status: StatusManutencao = StatusManutencao.ABERTO


class ManutencaoCreate(ManutencaoBase):
    pass


class ManutencaoSchema(ManutencaoBase):
    id: int
    created_at: datetime | None = None
    materiais: list[MaterialConsumoSchema] = []
    custo_total_materiais: float = 0.0
