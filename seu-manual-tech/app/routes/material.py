from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.core import get_db
from app.schemas.material import MaterialSchema, MaterialCreate
from app.services import material as service

router = APIRouter(prefix="/materiais", tags=["Materiais"])


@router.post("/", response_model=MaterialSchema, status_code=201)
def create_material(data: MaterialCreate, db: Session = Depends(get_db)):
    """Cria um novo material no catálogo"""
    existing = service.get_by_nome(db, data.nome)
    if existing:
        raise HTTPException(
            status_code=400, 
            detail=f"Já existe um material com o nome '{data.nome}'"
        )
    return service.create(db, data)


@router.get("/", response_model=list[MaterialSchema])
def list_materiais(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todos os materiais do catálogo"""
    return service.list_all(db, skip=skip, limit=limit)


@router.get("/{id}", response_model=MaterialSchema)
def get_material(id: int, db: Session = Depends(get_db)):
    """Busca um material por ID"""
    material = service.get_by_id(db, id)
    if not material:
        raise HTTPException(status_code=404, detail="Material não encontrado")
    return material
