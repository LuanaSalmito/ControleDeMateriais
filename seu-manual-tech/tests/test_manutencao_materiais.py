import pytest
from fastapi.testclient import TestClient


def test_manutencao_without_materials(client: TestClient):
    """Testa que uma manutenção sem materiais retorna custo zero"""
    
    response = client.post(
        "/manutencao/",
        json={"resumo": "Reparar parede", "status": "aberta"}
    )
    assert response.status_code == 201
    data = response.json()
    
   
    assert data["materiais"] == []
    assert data["custoTotalMateriais"] == 0.0


def test_add_material_to_manutencao(client: TestClient):
    """Testa adicionar um material a uma manutenção"""
    
    manutencao_response = client.post(
        "/manutencao/",
        json={"resumo": "Reparar parede", "status": "aberta"}
    )
    manutencao_id = manutencao_response.json()["id"]
    
    
    material_response = client.post(
        "/materiais/",
        json={"nome": "Cimento", "precoUnitario": 50.0}
    )
    material_id = material_response.json()["id"]
    
    
    response = client.post(
        f"/manutencao/{manutencao_id}/materiais",
        json={"materialId": material_id, "quantidade": 2}
    )
    assert response.status_code == 200
    data = response.json()
    
    
    assert len(data["materiais"]) == 1
    assert data["materiais"][0]["nome"] == "Cimento"
    assert data["materiais"][0]["quantidade"] == 2
    assert data["materiais"][0]["precoUnitario"] == 50.0
    assert data["materiais"][0]["custo"] == 100.0
    assert data["custoTotalMateriais"] == 100.0


def test_add_multiple_materials_to_manutencao(client: TestClient):
    """Testa adicionar múltiplos materiais a uma manutenção"""
    
    manutencao_response = client.post(
        "/manutencao/",
        json={"resumo": "Reparar parede norte", "status": "aberta"}
    )
    manutencao_id = manutencao_response.json()["id"]
    
    
    cimento = client.post(
        "/materiais/",
        json={"nome": "Cimento", "precoUnitario": 50.0}
    ).json()
    
    areia = client.post(
        "/materiais/",
        json={"nome": "Areia", "precoUnitario": 10.0}
    ).json()
    
    
    client.post(
        f"/manutencao/{manutencao_id}/materiais",
        json={"materialId": cimento["id"], "quantidade": 2}
    )
    
    client.post(
        f"/manutencao/{manutencao_id}/materiais",
        json={"materialId": areia["id"], "quantidade": 5}
    )
    
    
    response = client.get(f"/manutencao/{manutencao_id}")
    assert response.status_code == 200
    data = response.json()
    
    
    assert len(data["materiais"]) == 2
    
    
    cimento_data = next(m for m in data["materiais"] if m["nome"] == "Cimento")
    assert cimento_data["quantidade"] == 2
    assert cimento_data["precoUnitario"] == 50.0
    assert cimento_data["custo"] == 100.0
    
    
    areia_data = next(m for m in data["materiais"] if m["nome"] == "Areia")
    assert areia_data["quantidade"] == 5
    assert areia_data["precoUnitario"] == 10.0
    assert areia_data["custo"] == 50.0
    
    
    assert data["custoTotalMateriais"] == 150.0


@pytest.mark.parametrize("status", ["finalizada", "fechada", "concluida", "concluída"])
def test_cannot_add_material_to_finished_manutencao(client: TestClient, status: str):
    """Testa que não é possível adicionar materiais a manutenção com status finalizado"""
    
    manutencao_response = client.post(
        "/manutencao/",
        json={"resumo": "Reparar parede", "status": status}
    )
    manutencao_id = manutencao_response.json()["id"]
    
    
    material_response = client.post(
        "/materiais/",
        json={"nome": "Cimento", "precoUnitario": 50.0}
    )
    material_id = material_response.json()["id"]
    
    
    response = client.post(
        f"/manutencao/{manutencao_id}/materiais",
        json={"materialId": material_id, "quantidade": 2}
    )
    assert response.status_code == 400
    assert "finalizada" in response.json()["detail"].lower()


def test_cannot_add_nonexistent_material(client: TestClient):
    """Testa que não é possível adicionar material inexistente"""
   
    manutencao_response = client.post(
        "/manutencao/",
        json={"resumo": "Reparar parede", "status": "aberta"}
    )
    manutencao_id = manutencao_response.json()["id"]
    
   
    response = client.post(
        f"/manutencao/{manutencao_id}/materiais",
        json={"materialId": 999, "quantidade": 2}
    )
    assert response.status_code == 400
    assert "Material não encontrado" in response.json()["detail"]


def test_cannot_add_material_to_nonexistent_manutencao(client: TestClient):
    """Testa que não é possível adicionar material a manutenção inexistente"""
   
    material_response = client.post(
        "/materiais/",
        json={"nome": "Cimento", "precoUnitario": 50.0}
    )
    material_id = material_response.json()["id"]
    
    
    response = client.post(
        "/manutencao/999/materiais",
        json={"materialId": material_id, "quantidade": 2}
    )
    assert response.status_code == 400
    assert "Manutenção não encontrada" in response.json()["detail"]


def test_invalid_quantity(client: TestClient):
    """Testa validação de quantidade inválida"""
    
    manutencao = client.post(
        "/manutencao/",
        json={"resumo": "Reparar parede", "status": "aberta"}
    ).json()
    
    material = client.post(
        "/materiais/",
        json={"nome": "Cimento", "precoUnitario": 50.0}
    ).json()
    
 
    response = client.post(
        f"/manutencao/{manutencao['id']}/materiais",
        json={"materialId": material["id"], "quantidade": 0}
    )
    assert response.status_code == 422  #
    response = client.post(
        f"/manutencao/{manutencao['id']}/materiais",
        json={"materialId": material["id"], "quantidade": -5}
    )
    assert response.status_code == 422  