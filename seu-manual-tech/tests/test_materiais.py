import pytest
from fastapi.testclient import TestClient


def test_create_material(client: TestClient):
    """Testa criação de um material"""
    response = client.post(
        "/materiais/",
        json={"nome": "Cimento", "precoUnitario": 50.0}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == "Cimento"
    assert data["precoUnitario"] == 50.0
    assert "id" in data


def test_create_material_duplicate_name(client: TestClient):
    """Testa que não é possível criar materiais com nomes duplicados"""
    # Cria o primeiro material
    client.post("/materiais/", json={"nome": "Cimento", "precoUnitario": 50.0})
    
    # Tenta criar outro com o mesmo nome
    response = client.post(
        "/materiais/", 
        json={"nome": "Cimento", "precoUnitario": 60.0}
    )
    assert response.status_code == 400
    assert "Já existe um material" in response.json()["detail"]


def test_create_material_invalid_price(client: TestClient):
    """Testa validação de preço negativo ou zero"""
    response = client.post(
        "/materiais/",
        json={"nome": "Cimento", "precoUnitario": -10.0}
    )
    assert response.status_code == 422  # Validation error


def test_list_materiais(client: TestClient):
    """Testa listagem de materiais"""
    # Cria alguns materiais
    client.post("/materiais/", json={"nome": "Cimento", "precoUnitario": 50.0})
    client.post("/materiais/", json={"nome": "Areia", "precoUnitario": 10.0})
    client.post("/materiais/", json={"nome": "Tinta", "precoUnitario": 30.0})
    
    # Lista todos
    response = client.get("/materiais/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert data[0]["nome"] == "Cimento"
    assert data[1]["nome"] == "Areia"
    assert data[2]["nome"] == "Tinta"


def test_get_material_by_id(client: TestClient):
    """Testa busca de material por ID"""
    # Cria um material
    create_response = client.post(
        "/materiais/",
        json={"nome": "Cimento", "precoUnitario": 50.0}
    )
    material_id = create_response.json()["id"]
    
    # Busca por ID
    response = client.get(f"/materiais/{material_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == material_id
    assert data["nome"] == "Cimento"


def test_get_material_not_found(client: TestClient):
    """Testa busca de material inexistente"""
    response = client.get("/materiais/999")
    assert response.status_code == 404
