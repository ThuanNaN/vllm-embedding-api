"""Tests for the Bearer-token authentication middleware."""

import pytest

from tests.conftest import INVALID_API_KEY, VALID_API_KEY


class TestAuthentication:
    def test_missing_auth_header_returns_401(self, client):
        """No Authorization header → 401 Unauthorized."""
        resp = client.post(
            "/v1/embeddings",
            json={"input": "hello", "model": "BAAI/bge-small-en"},
        )
        assert resp.status_code == 401

    def test_invalid_api_key_returns_401(self, client):
        resp = client.post(
            "/v1/embeddings",
            json={"input": "hello", "model": "BAAI/bge-small-en"},
            headers={"Authorization": f"Bearer {INVALID_API_KEY}"},
        )
        assert resp.status_code == 401
        body = resp.json()
        assert body["error"]["message"] == "Unauthorized"
        assert body["error"]["type"] == "invalid_request_error"

    def test_valid_api_key_is_accepted(self, client):
        resp = client.post(
            "/v1/embeddings",
            json={"input": "hello", "model": "BAAI/bge-small-en"},
            headers={"Authorization": f"Bearer {VALID_API_KEY}"},
        )
        assert resp.status_code == 200

    def test_models_endpoint_requires_auth(self, client):
        resp = client.get("/v1/models")
        assert resp.status_code == 401

    def test_models_endpoint_rejects_invalid_key(self, client):
        resp = client.get(
            "/v1/models",
            headers={"Authorization": f"Bearer {INVALID_API_KEY}"},
        )
        assert resp.status_code == 401
