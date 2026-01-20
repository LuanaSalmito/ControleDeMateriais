#!/usr/bin/env python3
"""
Script de exemplo para demonstrar o uso da API de rastreamento de materiais.

Execute este script com o servidor rodando:
    uv run uvicorn app.main:app --reload

Em outro terminal:
    uv run python exemplo_uso.py
"""

import requests
import json
from typing import Any

BASE_URL = "http://127.0.0.1:8000"


def print_json(data: Any, title: str = ""):
    """Helper para imprimir JSON formatado"""
    if title:
        print(f"\n{'='*60}")
        print(f"  {title}")
        print('='*60)
    print(json.dumps(data, indent=2, ensure_ascii=False))


def main():
    print("\n🚀 Demonstração da API de Rastreamento de Materiais")
    print("="*60)
    
    # 1. Criar uma manutenção
    print("\n📝 1. Criando uma manutenção...")
    manutencao_data = {
        "resumo": "Reparar parede norte do prédio A",
        "status": "aberta"
    }
    response = requests.post(f"{BASE_URL}/manutencao/", json=manutencao_data)
    manutencao = response.json()
    print_json(manutencao, "Manutenção criada")
    manutencao_id = manutencao["id"]
    
    # 2. Criar materiais
    print("\n📦 2. Criando materiais no catálogo...")
    
    materiais_data = [
        {"nome": "Cimento Portland 50kg", "precoUnitario": 45.50},
        {"nome": "Areia Média (m³)", "precoUnitario": 120.00},
        {"nome": "Tinta Acrílica Branca 18L", "precoUnitario": 180.00},
        {"nome": "Tijolo Cerâmico 8 furos", "precoUnitario": 0.85},
    ]
    
    materiais = []
    for material_data in materiais_data:
        response = requests.post(f"{BASE_URL}/materiais/", json=material_data)
        material = response.json()
        materiais.append(material)
        print(f"  ✓ {material['nome']} - R$ {material['precoUnitario']:.2f}")
    
    # 3. Listar todos os materiais
    print("\n📋 3. Listando todos os materiais do catálogo...")
    response = requests.get(f"{BASE_URL}/materiais/")
    all_materiais = response.json()
    print_json(all_materiais, "Catálogo de Materiais")
    
    # 4. Adicionar materiais à manutenção
    print("\n🔨 4. Adicionando materiais à manutenção...")
    
    consumos = [
        {"materialId": materiais[0]["id"], "quantidade": 3},    # 3 sacos de cimento
        {"materialId": materiais[1]["id"], "quantidade": 0.5},  # 0.5 m³ de areia
        {"materialId": materiais[2]["id"], "quantidade": 2},    # 2 latas de tinta
        {"materialId": materiais[3]["id"], "quantidade": 150},  # 150 tijolos
    ]
    
    for consumo in consumos:
        response = requests.post(
            f"{BASE_URL}/manutencao/{manutencao_id}/materiais",
            json=consumo
        )
        if response.status_code == 200:
            # Encontra o nome do material
            material = next(m for m in materiais if m["id"] == consumo["materialId"])
            print(f"  ✓ {consumo['quantidade']}x {material['nome']}")
    
    # 5. Consultar manutenção com custos calculados
    print("\n💰 5. Consultando manutenção com custos calculados...")
    response = requests.get(f"{BASE_URL}/manutencao/{manutencao_id}")
    manutencao_final = response.json()
    print_json(manutencao_final, "Manutenção com Materiais e Custos")
    
    # 6. Exibir resumo dos custos
    print("\n📊 6. Resumo de Custos")
    print("="*60)
    for material in manutencao_final["materiais"]:
        print(f"  {material['nome']}")
        print(f"    Quantidade: {material['quantidade']}")
        print(f"    Preço unitário: R$ {material['precoUnitario']:.2f}")
        print(f"    Custo: R$ {material['custo']:.2f}")
        print()
    
    print(f"  {'CUSTO TOTAL:':>40} R$ {manutencao_final['custoTotalMateriais']:.2f}")
    print("="*60)
    
    # 7. Tentar adicionar material a manutenção finalizada (deve falhar)
    print("\n❌ 7. Testando proteção contra adição de materiais em manutenção finalizada...")
    
    # Criar manutenção finalizada
    response = requests.post(
        f"{BASE_URL}/manutencao/",
        json={"resumo": "Manutenção já concluída", "status": "finalizada"}
    )
    manutencao_finalizada = response.json()
    
    # Tentar adicionar material
    response = requests.post(
        f"{BASE_URL}/manutencao/{manutencao_finalizada['id']}/materiais",
        json={"materialId": materiais[0]["id"], "quantidade": 1}
    )
    
    if response.status_code == 400:
        print(f"  ✓ Proteção funcionando! Erro: {response.json()['detail']}")
    else:
        print(f"  ⚠️ Ops! Deveria ter falhado mas retornou status {response.status_code}")
    
    print("\n✅ Demonstração concluída com sucesso!")
    print("="*60)


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ Erro: Não foi possível conectar ao servidor.")
        print("   Certifique-se de que o servidor está rodando:")
        print("   uv run uvicorn app.main:app --reload")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
