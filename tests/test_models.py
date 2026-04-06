"""Tests for GET /v1/models."""

import os

from tests.conftest import VALID_API_KEY

AUTH = {"Authorization": f"Bearer {VALID_API_KEY}"}


class TestModels:
    def test_list_models_returns_correct_schema(self, client):
        resp = client.get("/v1/models", headers=AUTH)
        assert resp.status_code == 200
        body = resp.json()
        assert body["object"] == "list"
        assert isinstance(body["data"], list)
        assert len(body["data"]) >= 1

    def test_model_object_fields(self, client):
        resp = client.get("/v1/models", headers=AUTH)
        model = resp.json()["data"][0]
        assert "id" in model
        assert model["object"] == "model"
        assert model["owned_by"] == "local"

    def test_model_id_matches_env(self, client):
        expected_model = os.environ.get("MODEL_NAME", "BAAI/bge-small-en")
        resp = client.get("/v1/models", headers=AUTH)
        ids = [m["id"] for m in resp.json()["data"]]
        assert expected_model in ids
