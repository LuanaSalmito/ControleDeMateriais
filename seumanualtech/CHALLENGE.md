# Backend Challenge: Service Materials & Costs

## Overview

Welcome to the Seu Manual Backend Challenge!

We have provided a **boilerplate application** in this repository that uses FastAPI, SQLAlchemy 2.0, and Pydantic v2.

**Your Goal**: Implement a feature to track the cost of **materials** used in maintenance requests (`Manutencao`).

## The Feature

Currently, the system tracks Maintenance tickets (`Manutencao`), but not the materials consumed during the service. We need you to add:

1.  A **Material Catalog** (e.g., Cimento, Tijolo, Tinta).
2.  The ability to **consume materials** in a maintenance ticket, tracking the **quantity** used.
3.  Automatic calculation of the **Total Material Cost** for a ticket.

## Requirements

1.  **Material Management**:
    - Create and List materials.
    - Each material must have at least a name and a unit price.

2.  **Material Consumption**:
    - Add a specific quantity of a material to a maintenance ticket.
    - A maintenance ticket can have multiple materials, and the same material can be used in multiple maintenance tickets.

3.  **Cost Calculation**:
    - When retrieving a maintenance ticket, include the list of materials used and the **total cost** of those materials (Quantity \* Unit Price).

4.  **Business Rules**:
    - It shouldn't be possible to add materials to a maintenance ticket that is already "finished" (or equivalent final status).

## Expected API Behavior

We expect you to design the endpoints. However, the final response for a Maintenance ticket should look something like this:

### GET /manutencao/{id}

```json
{
  "id": 1,
  "resumo": "Reparar parede norte",
  "status": "aberta",
  "materiais": [
    {
      "id": 10,
      "nome": "Cimento",
      "quantidade": 2,
      "precoUnitario": 50.0,
      "custo": 100.0
    },
    {
      "id": 12,
      "nome": "Areia",
      "quantidade": 5,
      "precoUnitario": 10.0,
      "custo": 50.0
    }
  ],
  "custoTotalMateriais": 150.0
}
```

_Note: The field names in JSON can follow your preferred convention or the project's default (camelCase), as long as it is consistent._

## Openness & Justification

This challenge is designed to be open-ended, allowing you to express your technical style with freedom.

- **Freedom to Improve**: You are encouraged to improve the codebase using any technology, library, or architectural pattern you deem justifiable.
- **Justify Your Decisions**: Whatever choices you make, **you will be asked to explain the "why"**. Whether you add a new tool, refactor a module, or stick to the basics, providing a rationale for your decisions is crucial.

## Evaluation Criteria

- **Code Quality**: Clean, readable, and well-structured code.
- **Architecture**: Proper separation of concerns (Routes, Services, Models, Schemas).
- **Testing**: We value testing. Ensure your feature is covered by integration tests.
- **Correctness**: The feature works as described.

## Tech Stack

- **Language**: Python 3.12+
- **Framework**: FastAPI
- **Database**: SQLite (SQLAlchemy 2.0)
- **Validation**: Pydantic v2

## How to Run

1.  **Install Dependencies**:

    ```bash
    pip install uv
    uv sync
    ```

2.  **Run Development Server**:

    ```bash
    uv run uvicorn app.main:app --reload
    ```

    Open http://127.0.0.1:8000/docs to see the Swagger UI.

3.  **Run Tests**:
    ```bash
    uv run pytest
    ```

Good luck!
