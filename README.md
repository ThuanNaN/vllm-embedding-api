# vllm-embedding-api

High-performance embedding service powered by [vLLM](https://github.com/vllm-project/vllm) for scalable and low-latency vector generation. Exposes an **OpenAI-compatible REST API** so you can drop it in as a local replacement for `openai.Embedding.create`.

---

## Features

- **OpenAI-compatible** – `POST /v1/embeddings` and `GET /v1/models` follow the OpenAI API contract.
- **vLLM backend** – leverages vLLM's optimised inference engine for high-throughput batch embedding.
- **Bearer-token auth** – every endpoint is protected by a configurable API key.
- **Lazy model loading** – the vLLM model is loaded on the first request, so the server starts instantly (even without a GPU in test environments).
- **Accurate token counts** – uses `tiktoken` (`cl100k_base`) with a whitespace-split fallback.
- **Health endpoint** – `GET /health` for liveness probes.

---

## Prerequisites

| Requirement | Notes |
|---|---|
| Python 3.10+ | 3.11 recommended |
| CUDA-capable GPU | Required by vLLM at runtime; not needed for tests |
| [vLLM](https://docs.vllm.ai/en/latest/getting_started/installation.html) | Follow the official install guide for your CUDA version |

---

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/ThuanNaN/vllm-embedding-api.git
cd vllm-embedding-api

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Configuration

Copy the example environment file and fill in the values:

```bash
cp .env.example .env
```

| Variable | Default | Description |
|---|---|---|
| `API_KEY` | *(required)* | Secret Bearer token used to authenticate all requests |
| `MODEL_NAME` | `BAAI/bge-small-en` | HuggingFace model ID served by vLLM (must support the `embed` task) |

`.env.example`:
```dotenv
# Required: Secret key used to authenticate API requests (Bearer token)
API_KEY=your-secret-key

# Model served by vLLM (must support embedding task)
MODEL_NAME=BAAI/bge-small-en
```

---

## Running the service

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The interactive API docs are available at [http://localhost:8000/docs](http://localhost:8000/docs).

---

## API Reference

### `GET /health`
Liveness probe — no authentication required.

```bash
curl http://localhost:8000/health
# {"status":"ok"}
```

---

### `GET /v1/models`
Returns the list of available models.

```bash
curl http://localhost:8000/v1/models \
  -H "Authorization: Bearer your-secret-key"
```

<details>
<summary>Response</summary>

```json
{
  "object": "list",
  "data": [
    {
      "id": "BAAI/bge-small-en",
      "object": "model",
      "owned_by": "local"
    }
  ]
}
```
</details>

---

### `POST /v1/embeddings`
Generate embeddings for one or more texts.

**Request body**

| Field | Type | Required | Description |
|---|---|---|---|
| `input` | `string \| string[]` | ✅ | Text(s) to embed |
| `model` | `string` | ✅ | Model identifier (e.g. `BAAI/bge-small-en`) |
| `encoding_format` | `string` | ❌ | `"float"` (default) |

**cURL example**

```bash
curl http://localhost:8000/v1/embeddings \
  -H "Authorization: Bearer your-secret-key" \
  -H "Content-Type: application/json" \
  -d '{
    "input": ["Hello, world!", "vLLM is fast."],
    "model": "BAAI/bge-small-en"
  }'
```

<details>
<summary>Response</summary>

```json
{
  "object": "list",
  "data": [
    {"object": "embedding", "embedding": [0.021, -0.003, ...], "index": 0},
    {"object": "embedding", "embedding": [0.014,  0.008, ...], "index": 1}
  ],
  "model": "BAAI/bge-small-en",
  "usage": {
    "prompt_tokens": 8,
    "total_tokens": 8
  }
}
```
</details>

**Python (openai SDK)**

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="your-secret-key",
)

response = client.embeddings.create(
    model="BAAI/bge-small-en",
    input=["Hello, world!", "vLLM is fast."],
)

for item in response.data:
    print(f"index={item.index}, dims={len(item.embedding)}")
```

---

## Project structure

```
vllm-embedding-api/
├── app/
│   ├── main.py                  # FastAPI application & exception handlers
│   ├── config.py                # Environment-variable configuration
│   ├── dependencies.py          # Bearer-token authentication dependency
│   ├── api/
│   │   └── v1/
│   │       ├── embeddings.py    # POST /v1/embeddings
│   │       ├── models.py        # GET  /v1/models
│   │       └── chat.py          # Placeholder for future chat completions
│   ├── schemas/
│   │   ├── embeddings.py        # Pydantic request/response models
│   │   └── models.py            # Pydantic model-list schemas
│   ├── services/
│   │   └── embedding_service.py # vLLM model wrapper
│   └── utils/
│       └── tokens.py            # Token counting (tiktoken / fallback)
├── scripts/
│   └── export_openapi.py        # Exports openapi.json for docs generation
├── tests/
│   ├── conftest.py              # Shared fixtures (mocked vLLM backend)
│   ├── test_auth.py             # Authentication tests
│   ├── test_embeddings.py       # Embedding endpoint tests
│   └── test_models.py           # Models endpoint tests
├── .env.example                 # Environment variable template
├── requirements.txt             # Runtime dependencies
├── requirements-dev.txt         # Development & test dependencies
└── requirements-docs.txt        # Documentation generation dependencies
```

---

## Running tests

Tests mock the vLLM backend so **no GPU is required**.

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run the full test suite
python -m pytest tests/ -v
```

---

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

---

## License

This project is open-source. See the repository for license details.
