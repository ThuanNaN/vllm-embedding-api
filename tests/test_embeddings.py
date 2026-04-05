"""Tests for POST /v1/embeddings."""

from tests.conftest import FAKE_EMBEDDING, VALID_API_KEY

AUTH = {"Authorization": f"Bearer {VALID_API_KEY}"}


class TestEmbeddings:
    def test_single_string_input(self, client):
        resp = client.post(
            "/v1/embeddings",
            json={"input": "hello world", "model": "BAAI/bge-small-en"},
            headers=AUTH,
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["object"] == "list"
        assert body["model"] == "BAAI/bge-small-en"
        assert len(body["data"]) == 1
        item = body["data"][0]
        assert item["object"] == "embedding"
        assert item["index"] == 0
        assert item["embedding"] == FAKE_EMBEDDING
        assert body["usage"]["prompt_tokens"] > 0
        assert body["usage"]["total_tokens"] == body["usage"]["prompt_tokens"]

    def test_list_string_input(self, client, mock_generate_embeddings):
        """Multiple inputs → index values must match position."""
        mock_generate_embeddings.return_value = [FAKE_EMBEDDING, FAKE_EMBEDDING]
        resp = client.post(
            "/v1/embeddings",
            json={
                "input": ["hello world", "foo bar"],
                "model": "BAAI/bge-small-en",
            },
            headers=AUTH,
        )
        assert resp.status_code == 200
        body = resp.json()
        assert len(body["data"]) == 2
        assert body["data"][0]["index"] == 0
        assert body["data"][1]["index"] == 1

    def test_response_schema_fields(self, client, mock_generate_embeddings):
        mock_generate_embeddings.return_value = [FAKE_EMBEDDING]
        resp = client.post(
            "/v1/embeddings",
            json={"input": "test", "model": "my-model"},
            headers=AUTH,
        )
        body = resp.json()
        # Top-level fields
        assert set(body.keys()) >= {"object", "data", "model", "usage"}
        # Usage fields
        assert set(body["usage"].keys()) >= {"prompt_tokens", "total_tokens"}
        # Data item fields
        item = body["data"][0]
        assert set(item.keys()) >= {"object", "embedding", "index"}

    def test_model_field_reflects_request(self, client, mock_generate_embeddings):
        mock_generate_embeddings.return_value = [FAKE_EMBEDDING]
        resp = client.post(
            "/v1/embeddings",
            json={"input": "hi", "model": "custom-model-name"},
            headers=AUTH,
        )
        assert resp.json()["model"] == "custom-model-name"

    def test_invalid_request_body_returns_422(self, client):
        """Missing required fields → 422 Unprocessable Entity."""
        resp = client.post(
            "/v1/embeddings",
            json={"model": "BAAI/bge-small-en"},  # missing 'input'
            headers=AUTH,
        )
        assert resp.status_code == 422
