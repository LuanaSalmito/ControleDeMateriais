from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.material import Material, ManutencaoMaterial
from app.models.manutencao import Manutencao
from app.schemas.material import MaterialCreate, MaterialConsumoCreate


def get_by_id(db: Session, id: int) -> Material | None:
    """Busca um material por ID"""
    return db.scalar(select(Material).where(Material.id == id))


def get_by_nome(db: Session, nome: str) -> Material | None:
    """Busca um material por nome"""
    return db.scalar(select(Material).where(Material.nome == nome))


def list_all(db: Session, skip: int = 0, limit: int = 100) -> list[Material]:
    """Lista todos os materiais"""
    return list(db.scalars(select(Material).offset(skip).limit(limit)).all())


def create(db: Session, schema: MaterialCreate) -> Material:
    """Cria um novo material"""
    db_obj = Material(**schema.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def adicionar_material_manutencao(
    db: Session, 
    manutencao_id: int, 
    schema: MaterialConsumoCreate
) -> ManutencaoMaterial:
    """
    Adiciona um material a uma manutenção.
    
    Raises:
        ValueError: Se a manutenção não existir, estiver finalizada, ou o material não existir
    """
    manutencao = db.scalar(select(Manutencao).where(Manutencao.id == manutencao_id))
    if not manutencao:
        raise ValueError("Manutenção não encontrada")
    
    if manutencao.status in ["finalizada", "concluida", "fechada"]:
        raise ValueError("Não é possível adicionar materiais a uma manutenção finalizada")
    
    
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
