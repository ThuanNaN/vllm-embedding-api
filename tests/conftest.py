"""Shared pytest fixtures for the vllm-embedding-api test suite."""

import os
from unittest.mock import MagicMock, patch

import pytest

# Set required environment variables BEFORE importing the app so that
# app.config picks them up at module-load time.
os.environ.setdefault("API_KEY", "test-secret-key")
os.environ.setdefault("MODEL_NAME", "BAAI/bge-small-en")

VALID_API_KEY = "test-secret-key"
INVALID_API_KEY = "wrong-key"

FAKE_EMBEDDING = [0.1, 0.2, 0.3]


@pytest.fixture(scope="session")
def mock_generate_embeddings():
    """Patch the vLLM backend for the entire test session."""
    with patch(
        "app.api.v1.embeddings.generate_embeddings",
        return_value=[FAKE_EMBEDDING],
    ) as mock:
        yield mock


@pytest.fixture(scope="session")
def client(mock_generate_embeddings):
    """A TestClient wired up with the mocked embedding backend."""
    from fastapi.testclient import TestClient

    from app.main import app

    return TestClient(app)
