from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.manutencao import Manutencao
from app.schemas.manutencao import ManutencaoCreate, ManutencaoSchema
from app.schemas.material import MaterialConsumoSchema


def get_by_id(db: Session, id: int) -> Manutencao | None:
    return db.scalar(select(Manutencao).where(Manutencao.id == id))


def get_by_id_with_materials(db: Session, id: int) -> ManutencaoSchema | None:
    """
    Busca uma manutenção por ID e retorna com os materiais e custo total calculado
    """
    manutencao = db.scalar(select(Manutencao).where(Manutencao.id == id))
    if not manutencao:
        return None
    
    # Processa os materiais consumidos
    materiais_schema = []
    custo_total = 0.0
    
    for consumo in manutencao.materiais_consumidos:
        custo = float(consumo.quantidade) * float(consumo.material.preco_unitario)
        custo_total += custo
        
        material_consumo = MaterialConsumoSchema(
            id=consumo.material.id,
            nome=consumo.material.nome,
            quantidade=float(consumo.quantidade),
            preco_unitario=float(consumo.material.preco_unitario),
            custo=custo
        )
        materiais_schema.append(material_consumo)
    
    # Cria o schema de resposta
    return ManutencaoSchema(
        id=manutencao.id,
        resumo=manutencao.resumo,
        status=manutencao.status,
        created_at=manutencao.criado_em,
        materiais=materiais_schema,
        custo_total_materiais=custo_total
    )


def create(db: Session, schema: ManutencaoCreate) -> Manutencao:
    db_obj = Manutencao(**schema.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
