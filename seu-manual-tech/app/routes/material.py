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


@router.post("/bulk", response_model=list[MaterialSchema], status_code=201)
def create_materials_bulk(data: list[MaterialCreate], db: Session = Depends(get_db)):
    """
    Cria múltiplos materiais de uma vez
    
    - Materiais com nomes duplicados (já existentes) serão ignorados
    - Retorna apenas os materiais criados com sucesso
    """
    if not data:
        raise HTTPException(status_code=400, detail="Lista de materiais não pode ser vazia")
    
    created = service.create_bulk(db, data)
    
    if not created:
        raise HTTPException(
            status_code=400, 
            detail="Nenhum material foi criado. Todos os nomes já existem no catálogo."
        )
    
    return created


@router.get("/", response_model=list[MaterialSchema])
def list_materiais(
    skip: int = 0, 
    limit: int = 100, 
    nome: str | None = None,
    ordenar_por: str = "nome",
    ordem: str = "asc",
    db: Session = Depends(get_db)
):
    """
    Lista todos os materiais do catálogo com filtros e ordenação
    
    - **skip**: Número de registros a pular (paginação)
    - **limit**: Número máximo de registros a retornar (máx: 100)
    - **nome**: Filtro parcial por nome (busca case-insensitive)
    - **ordenar_por**: Campo para ordenação ('nome' ou 'preco_unitario')
    - **ordem**: Direção da ordenação ('asc' ou 'desc')
    """
    return service.list_all(
        db, 
        skip=skip, 
        limit=limit, 
        nome=nome,
        ordenar_por=ordenar_por,
        ordem=ordem
    )


@router.get("/{id}", response_model=MaterialSchema)
def get_material(id: int, db: Session = Depends(get_db)):
    """Busca um material por ID"""
    material = service.get_by_id(db, id)
    if not material:
        raise HTTPException(status_code=404, detail="Material não encontrado")
    return material


@router.put("/{id}", response_model=MaterialSchema)
def update_material(id: int, data: MaterialCreate, db: Session = Depends(get_db)):
    """Atualiza um material existente"""
    existing = service.get_by_nome(db, data.nome)
    if existing and existing.id != id:
        raise HTTPException(
            status_code=400, 
            detail=f"Já existe outro material com o nome '{data.nome}'"
        )
    
    material = service.update(db, id, data)
    if not material:
        raise HTTPException(status_code=404, detail="Material não encontrado")
    return material


@router.delete("/{id}", status_code=204)
def delete_material(id: int, db: Session = Depends(get_db)):
    """Deleta um material"""
    deleted = service.delete(db, id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Material não encontrado")
    return None
