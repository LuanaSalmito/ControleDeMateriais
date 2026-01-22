# Seu Manual Backend Challenge

This repository contains a boilerplate FastAPI application designed to mirror the architecture of our main services.

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install uv
    uv sync
    ```

2.  **Run Development Server**:
    ```bash
    uv run uvicorn app.main:app --reload
    ```
    Access Swagger UI at http://127.0.0.1:8000/docs

3.  **Run Tests**:
    ```bash
    uv run pytest
    ```

## The Challenge

Please refer to [CHALLENGE.md](CHALLENGE.md) for the instructions.

## Project Structure

- `app/models`: SQLAlchemy ORM models.
- `app/schemas`: Pydantic schemas (request/response).
- `app/services`: Business logic layer.
- `app/routes`: API endpoints.
- `app/database`: DB configuration.
- `tests/`: Pytest tests.
