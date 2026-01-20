# Justificativas Técnicas

Este documento explica as decisões técnicas tomadas durante a implementação da funcionalidade de rastreamento de custos de materiais.

## Arquitetura e Design

### 1. Tabela de Associação com Dados Adicionais

**Decisão**: Criar uma entidade `ManutencaoMaterial` em vez de usar um relacionamento many-to-many simples.

**Justificativa**:
- Precisamos armazenar a **quantidade** de cada material usado em cada manutenção
- A tabela de associação permite adicionar metadados (quantidade, data de consumo futura, etc.)
- Facilita auditoria e rastreabilidade
- Permite extender facilmente no futuro (ex: adicionar data de consumo, responsável, etc.)

**Alternativa considerada**: Usar um relacionamento many-to-many simples e armazenar a quantidade como atributo extra do relacionamento. Porém, SQLAlchemy 2.0 torna mais explícito e manutenível criar uma classe dedicada.

### 2. Cálculo de Custo na Camada de Service

**Decisão**: Calcular o custo total na camada de service (`get_by_id_with_materials`) em vez de no modelo ou schema.

**Justificativa**:
- **Separação de responsabilidades**: A lógica de negócio fica na camada de service
- **Testabilidade**: Fácil testar o cálculo isoladamente
- **Flexibilidade**: Se o cálculo precisar de regras mais complexas (descontos, taxas, etc.), é fácil modificar
- **Performance**: Evita cálculos desnecessários quando não precisamos do custo total

**Alternativa considerada**: Usar `@property` no modelo SQLAlchemy ou `@computed_field` no Pydantic. Porém, isso acoplaria a lógica de negócio ao modelo ou schema, tornando-o menos testável.

### 3. Validações com Pydantic v2

**Decisão**: Usar `Field` com validadores (`gt=0`, `min_length`, etc.) nos schemas.

**Justificativa**:
- **Validação automática**: Pydantic valida os dados antes de chegarem ao service
- **Documentação automática**: As validações aparecem automaticamente no Swagger
- **Mensagens de erro claras**: Pydantic gera mensagens de erro descritivas
- **Type safety**: Garantimos que os dados estão no formato correto

**Exemplo**:
```python
preco_unitario: float = Field(..., gt=0, description="Preço unitário do material")
```

### 4. Uso de `lazy="selectin"` no Relacionamento

**Decisão**: Configurar o relacionamento `materiais_consumidos` com `lazy="selectin"`.

**Justificativa**:
- **Evita N+1 queries**: Carrega os materiais relacionados em uma única query adicional
- **Performance**: Muito mais eficiente do que lazy loading padrão
- **Previsibilidade**: Sabemos exatamente quantas queries serão executadas

**Alternativa considerada**: Usar `lazy="joined"` (join automático). Porém, `selectin` é mais eficiente para relacionamentos one-to-many.

**Referência**: [SQLAlchemy - Relationship Loading Techniques](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#selectin-eager-loading)

### 5. Tipo `Numeric` para Valores Monetários

**Decisão**: Usar `Numeric(10, 2)` em vez de `Float` para preços e custos.

**Justificativa**:
- **Precisão decimal**: Evita erros de arredondamento típicos de floats
- **Padrão da indústria**: Valores monetários devem sempre usar decimal/numeric
- **Consistência**: 2 casas decimais são suficientes para reais (R$)

**Alternativa considerada**: Usar `Float`. Porém, isso pode causar erros de arredondamento:
```python
# Exemplo de problema com float:
>>> 0.1 + 0.2
0.30000000000000004
```

### 6. Retornar Schema ao Invés de Model nas Routes

**Decisão**: O service `get_by_id_with_materials` retorna `ManutencaoSchema` ao invés de `Manutencao`.

**Justificativa**:
- **Cálculos adicionais**: Precisamos processar os materiais e calcular custos
- **Controle de serialização**: Temos controle total sobre o que é retornado
- **Flexibilidade**: Podemos adicionar campos calculados facilmente
- **Desacoplamento**: A API não depende diretamente da estrutura do banco

**Alternativa considerada**: Usar `@computed_field` no schema e passar o model. Porém, isso limitaria nossa flexibilidade para cálculos complexos.

### 7. Validação de Status na Camada de Service

**Decisão**: Validar se a manutenção está finalizada no service, não no modelo.

**Justificativa**:
- **Flexibilidade**: Status pode mudar no futuro (concluída, fechada, cancelada, etc.)
- **Mensagens de erro personalizadas**: Podemos retornar erros mais descritivos
- **Testabilidade**: Fácil testar essa regra de negócio

**Código**:
```python
if manutencao.status in ["finalizada", "concluida", "fechada"]:
    raise ValueError("Não é possível adicionar materiais a uma manutenção finalizada")
```

### 8. Endpoint Dedicado para Adicionar Materiais

**Decisão**: Criar `POST /manutencao/{id}/materiais` ao invés de incluir materiais na criação da manutenção.

**Justificativa**:
- **Realismo**: Materiais são consumidos durante o serviço, não na criação do chamado
- **Granularidade**: Permite adicionar materiais um de cada vez conforme são usados
- **Auditoria**: Facilita rastrear quando cada material foi adicionado (preparação futura)
- **Simplicidade**: Endpoints têm uma responsabilidade única e clara

**Alternativa considerada**: Aceitar lista de materiais em `POST /manutencao/`. Porém, isso não reflete o fluxo de trabalho real.

### 9. Uso Consistente de camelCase

**Decisão**: Manter o padrão `CamelSchema` do projeto.

**Justificativa**:
- **Consistência**: Segue o padrão já estabelecido no projeto
- **Convenção web**: camelCase é comum em APIs REST e JSON
- **Configuração automática**: Pydantic converte snake_case para camelCase automaticamente

**Configuração**:
```python
class CamelSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel, 
        populate_by_name=True, 
        from_attributes=True
    )
```

### 10. Testes Abrangentes

**Decisão**: Criar testes para todos os cenários (sucesso e falha).

**Justificativa**:
- **Confiabilidade**: Garante que a funcionalidade funciona como esperado
- **Documentação viva**: Os testes documentam o comportamento esperado
- **Regressão**: Previne bugs ao fazer mudanças futuras
- **Casos de erro**: Testa validações e regras de negócio

**Cenários testados**:
- ✅ Criar e listar materiais
- ✅ Validações (preço positivo, quantidade positiva, nome único)
- ✅ Adicionar materiais a manutenção
- ✅ Cálculo de custos
- ✅ Proteção contra modificação de manutenção finalizada
- ✅ Tratamento de recursos inexistentes

## Possíveis Melhorias Futuras

### 1. Histórico de Alterações
Adicionar auditoria para rastrear quando cada material foi adicionado e por quem.

### 2. Gestão de Estoque
Integrar com sistema de estoque para controlar disponibilidade de materiais.

### 3. Categorização de Materiais
Adicionar categorias (elétrica, hidráulica, alvenaria, etc.) para facilitar relatórios.

### 4. Paginação
Adicionar paginação na listagem de materiais quando o catálogo crescer.

### 5. Unidades de Medida
Adicionar campo para unidade de medida (kg, m³, litro, unidade, etc.).

### 6. Descontos e Taxas
Permitir aplicar descontos ou taxas adicionais no cálculo de custos.

### 7. Relatórios
Criar endpoints para relatórios de custos por período, por tipo de manutenção, etc.

### 8. Soft Delete
Implementar soft delete para materiais (flag_ativo) em vez de deletar permanentemente.

## Conclusão

As decisões tomadas priorizam:
- ✅ **Manutenibilidade**: Código limpo e bem estruturado
- ✅ **Testabilidade**: Lógica de negócio testável
- ✅ **Escalabilidade**: Fácil adicionar funcionalidades futuras
- ✅ **Performance**: Uso eficiente de queries
- ✅ **Clareza**: Código autoexplicativo e bem documentado

Todas as escolhas seguem as melhores práticas de desenvolvimento com FastAPI, SQLAlchemy 2.0 e Pydantic v2.
