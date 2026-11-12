# ADR 0002: Build the API with FastAPI

## Context
The service needs a small REST API with input validation, easy testing and generated documentation.

## Decision
Use FastAPI with uvicorn.

## Consequences
- Typed endpoints and automatic OpenAPI docs at /docs
- Built-in test client for fast unit tests
- Async support for the upstream calls
- Adds a Python runtime dependency, which the Docker image covers