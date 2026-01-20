from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.core import get_db
from app.schemas.manutencao import ManutencaoSchema, ManutencaoCreate
from app.schemas.material import MaterialConsumoCreate
from app.services import manutencao as service
from app.services import material as material_service

router = APIRouter(prefix="/manutencao", tags=["Manutencao"])


@router.post("/", response_model=ManutencaoSchema)
def create_manutencao(data: ManutencaoCreate, db: Session = Depends(get_db)):
    manutencao = service.create(db, data)
    # Retorna a manutenção com materiais (vazio inicialmente)
    return service.get_by_id_with_materials(db, manutencao.id)


@router.get("/{id}", response_model=ManutencaoSchema)
def get_manutencao(id: int, db: Session = Depends(get_db)):
    obj = service.get_by_id_with_materials(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Manutencao not found")
    return obj


@router.post("/{id}/materiais", response_model=ManutencaoSchema)
def adicionar_material_manutencao(
    id: int, 
    data: MaterialConsumoCreate, 
    db: Session = Depends(get_db)
):
    """Adiciona um material a uma manutenção"""
    try:
        material_service.adicionar_material_manutencao(db, id, data)
        # Retorna a manutenção atualizada com os materiais
        manutencao = service.get_by_id_with_materials(db, id)
        if not manutencao:
            raise HTTPException(status_code=404, detail="Manutencao not found")
        return manutencao
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
