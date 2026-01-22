# Alembic Migrations

Este projeto usa Alembic para gerenciar migrations do banco de dados.

## Comandos Úteis

### Criar uma nova migration (auto-generate)
```bash
uv run python -m alembic revision --autogenerate -m "Descrição da mudança"
```

### Aplicar migrations pendentes
```bash
uv run python -m alembic upgrade head
```

### Reverter última migration
```bash
uv run python -m alembic downgrade -1
```

### Ver histórico de migrations
```bash
uv run python -m alembic history
```

### Ver status atual
```bash
uv run python -m alembic current
```

### Criar migration vazia (para mudanças manuais)
```bash
uv run python -m alembic revision -m "Descrição"
```

## Workflow de Desenvolvimento

1. **Modificar Models**: Altere os models em `app/models/`
2. **Gerar Migration**: `uv run python -m alembic revision --autogenerate -m "descrição"`
3. **Revisar Migration**: Verifique o arquivo gerado em `alembic/versions/`
4. **Aplicar Migration**: `uv run python -m alembic upgrade head`
5. **Testar**: Execute os testes para garantir que tudo funciona

## Importante

- **NUNCA** use `Base.metadata.create_all()` em produção
- **SEMPRE** revise migrations auto-geradas antes de aplicar
- **SEMPRE** crie backup do banco antes de migrations em produção
- Migrations devem ser versionadas no git

## Estrutura

```
alembic/
├── versions/          # Arquivos de migration
├── env.py            # Configuração do ambiente Alembic
├── script.py.mako    # Template para novas migrations
└── README            # Este arquivo
```

## Configuração

A configuração do banco de dados é obtida automaticamente de `app.config.settings.DATABASE_URL`.

Para alterar o banco de dados, configure a variável de ambiente `DATABASE_URL` ou edite o arquivo `.env`.
