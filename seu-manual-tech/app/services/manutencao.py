from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.manutencao import Manutencao
from app.schemas.manutencao import ManutencaoCreate, ManutencaoSchema
from app.schemas.material import MaterialConsumoSchema


def get_by_id(db: Session, id: int) -> Manutencao | None:
    return db.scalar(select(Manutencao).where(Manutencao.id == id))


def get_by_id_with_materials(db: Session, id: int) -> ManutencaoSchema | None:
    manutencao = db.scalar(select(Manutencao).where(Manutencao.id == id))
    if not manutencao:
        return None
    
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
    
    return ManutencaoSchema(
        id=manutencao.id,
        resumo=manutencao.resumo,
        status=manutencao.status,
        created_at=manutencao.criado_em,
        materiais=materiais_schema,
        custo_total_materiais=custo_total
    )


def list_all(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    status: str | None = None
) -> list[ManutencaoSchema]:
    query = select(Manutencao)
    
    if status:
        query = query.where(Manutencao.status == status)
    
    query = query.order_by(Manutencao.criado_em.desc())
    query = query.offset(skip).limit(limit)
    
    manutencoes = list(db.scalars(query).all())
    
    result = []
    for manutencao in manutencoes:
        manutencao_schema = get_by_id_with_materials(db, manutencao.id)
        if manutencao_schema:
            result.append(manutencao_schema)
    
    return result


def create(db: Session, schema: ManutencaoCreate) -> Manutencao:
    db_obj = Manutencao(**schema.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def create_bulk(db: Session, schemas: list[ManutencaoCreate]) -> list[ManutencaoSchema]:
    created_manutencoes = []
    
    for schema in schemas:
        db_obj = Manutencao(**schema.model_dump())
        db.add(db_obj)
        created_manutencoes.append(db_obj)
    
    db.commit()
    
    result = []
    for manutencao in created_manutencoes:
        db.refresh(manutencao)
        manutencao_schema = get_by_id_with_materials(db, manutencao.id)
        if manutencao_schema:
            result.append(manutencao_schema)
    
    return result


def update(db: Session, id: int, schema: ManutencaoCreate) -> Manutencao | None:
    manutencao = get_by_id(db, id)
    if not manutencao:
        return None
    
    for key, value in schema.model_dump().items():
        setattr(manutencao, key, value)
    
    db.commit()
    db.refresh(manutencao)
    return manutencao


def delete(db: Session, id: int) -> bool:
    manutencao = get_by_id(db, id)
    if not manutencao:
        return False
    
    db.delete(manutencao)
    db.commit()
    return True
