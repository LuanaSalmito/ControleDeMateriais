from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.core import get_db
from app.schemas.manutencao import ManutencaoSchema, ManutencaoCreate
from app.schemas.material import MaterialConsumoCreate
from app.services import manutencao as service
from app.services import material as material_service

router = APIRouter(prefix="/manutencao", tags=["Manutencao"])


@router.post("/", response_model=ManutencaoSchema, status_code=201)
def create_manutencao(data: ManutencaoCreate, db: Session = Depends(get_db)):
    """Cria uma nova manutenção"""
    manutencao = service.create(db, data)
    return service.get_by_id_with_materials(db, manutencao.id)


@router.post("/bulk", response_model=list[ManutencaoSchema], status_code=201)
def create_manutencoes_bulk(data: list[ManutencaoCreate], db: Session = Depends(get_db)):
    """
    Cria múltiplas manutenções de uma vez
    
    - Todas as manutenções serão criadas em uma única transação
    - Retorna a lista de manutenções criadas com seus materiais (vazio inicialmente)
    """
    if not data:
        raise HTTPException(status_code=400, detail="Lista de manutenções não pode ser vazia")
    
    created = service.create_bulk(db, data)
    return created


@router.get("/", response_model=list[ManutencaoSchema])
def list_manutencoes(
    skip: int = 0, 
    limit: int = 100,
    status: str | None = None,
    db: Session = Depends(get_db)
):
    """
    Lista todas as manutenções com filtros
    
    - **skip**: Número de registros a pular (paginação)
    - **limit**: Número máximo de registros a retornar (máx: 100)
    - **status**: Filtro por status da manutenção (ex: 'aberta', 'FINALIZADA')
    """
    return service.list_all(db, skip=skip, limit=limit, status=status)


@router.get("/{id}", response_model=ManutencaoSchema)
def get_manutencao(id: int, db: Session = Depends(get_db)):
    """Busca uma manutenção por ID com materiais e custo total"""
    obj = service.get_by_id_with_materials(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Manutenção não encontrada")
    return obj


@router.put("/{id}", response_model=ManutencaoSchema)
def update_manutencao(id: int, data: ManutencaoCreate, db: Session = Depends(get_db)):
    """Atualiza uma manutenção existente"""
    manutencao = service.update(db, id, data)
    if not manutencao:
        raise HTTPException(status_code=404, detail="Manutenção não encontrada")
    return service.get_by_id_with_materials(db, id)


@router.delete("/{id}", status_code=204)
def delete_manutencao(id: int, db: Session = Depends(get_db)):
    """Deleta uma manutenção"""
    deleted = service.delete(db, id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Manutenção não encontrada")
    return None


@router.post("/{id}/materiais", response_model=ManutencaoSchema)
def adicionar_material_manutencao(
    id: int, 
    data: MaterialConsumoCreate, 
    db: Session = Depends(get_db)
):
    """Adiciona um material a uma manutenção"""
    try:
        material_service.adicionar_material_manutencao(db, id, data)
        manutencao = service.get_by_id_with_materials(db, id)
        if not manutencao:
            raise HTTPException(status_code=404, detail="Manutencao not found")
        return manutencao
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
