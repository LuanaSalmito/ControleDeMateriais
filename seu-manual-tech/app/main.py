from fastapi import FastAPI
from app.database.core import engine, Base
from app.routes import manutencao, material

# Create tables on startup (simplification for challenge)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Controle de Materiais",
    description="""
    ## API para Gerenciamento de Manutenções e Materiais
    
    Esta API permite:
    
    ### 📦 Materiais
    * Criar, listar, atualizar e deletar materiais
    * Filtrar materiais por nome
    * Ordenar por nome ou preço
    * Paginação de resultados
    
    ### 🔧 Manutenções
    * Criar, listar, atualizar e deletar manutenções
    * Adicionar materiais a manutenções
    * Calcular custo total de materiais
    * Filtrar por status
    * Validação de regras de negócio
    
    ### 💰 Cálculo de Custos
    * Custo automático: quantidade × preço unitário
    * Custo total por manutenção
    
    ### 🔒 Regras de Negócio
    * Não é possível adicionar materiais a manutenções finalizadas
    * Validação de dados obrigatórios
    * Preços devem ser positivos
    """,
    version="1.0.0",
    contact={
        "name": "Seu Manual Tech",
        "url": "https://github.com/seu-usuario/seu-manual-tech",
    }
)

app.include_router(manutencao.router)
app.include_router(material.router)


@app.get("/")
def health():
    return {"status": "ok"}
