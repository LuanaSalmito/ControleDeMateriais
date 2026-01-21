from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.material import Material
from app.models.manutencao_material import ManutencaoMaterial
from app.models.manutencao import Manutencao
from app.schemas.material import MaterialCreate, MaterialConsumoCreate


def get_by_id(db: Session, id: int) -> Material | None:
    return db.scalar(select(Material).where(Material.id == id))


def get_by_nome(db: Session, nome: str) -> Material | None:
    return db.scalar(select(Material).where(Material.nome == nome))


def list_all(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    nome: str | None = None,
    ordenar_por: str = "nome",
    ordem: str = "asc"
) -> list[Material]:
    query = select(Material)
    
    if nome:
        query = query.where(Material.nome.ilike(f"%{nome}%"))
    
    if ordenar_por == "preco_unitario":
        order_column = Material.preco_unitario
    else:
        order_column = Material.nome
    
    if ordem == "desc":
        query = query.order_by(order_column.desc())
    else:
        query = query.order_by(order_column.asc())
    
    query = query.offset(skip).limit(limit)
    
    return list(db.scalars(query).all())


def create(db: Session, schema: MaterialCreate) -> Material:
    db_obj = Material(**schema.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def create_bulk(db: Session, schemas: list[MaterialCreate]) -> list[Material]:
    created_materials = []
    
    for schema in schemas:
        existing = get_by_nome(db, schema.nome)
        if not existing:
            db_obj = Material(**schema.model_dump())
            db.add(db_obj)
            created_materials.append(db_obj)
    
    db.commit()
    
    for material in created_materials:
        db.refresh(material)
    
    return created_materials


def update(db: Session, id: int, schema: MaterialCreate) -> Material | None:
    material = get_by_id(db, id)
    if not material:
        return None
    
    for key, value in schema.model_dump().items():
        setattr(material, key, value)
    
    db.commit()
    db.refresh(material)
    return material


def delete(db: Session, id: int) -> bool:
    material = get_by_id(db, id)
    if not material:
        return False
    
    db.delete(material)
    db.commit()
    return True


def adicionar_material_manutencao(
    db: Session, 
    manutencao_id: int, 
    schema: MaterialConsumoCreate
) -> ManutencaoMaterial:
    manutencao = db.scalar(select(Manutencao).where(Manutencao.id == manutencao_id))
    if not manutencao:
        raise ValueError("Manutenção não encontrada")
    
    status_finalizados = ["finalizada", "fechada", "concluida", "concluída"]
    if manutencao.status.lower() in status_finalizados:
        raise ValueError("Não é possível adicionar materiais a uma manutenção finalizada.")
    
    material = db.scalar(select(Material).where(Material.id == schema.material_id))
    if not material:
        raise ValueError("Material não encontrado")
    
    db_obj = ManutencaoMaterial(
        manutencao_id=manutencao_id,
        material_id=schema.material_id,
        quantidade=schema.quantidade
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
