"""vLLM-backed embedding service.

The vLLM ``LLM`` instance is created lazily on the first request so that the
FastAPI application can start and be tested without a GPU present (tests mock
``generate_embeddings`` directly).
"""

import logging
from typing import List

from app.config import MODEL_NAME

logger = logging.getLogger(__name__)

_model = None


def _get_model():
    global _model
    if _model is None:
        try:
            from vllm import LLM  # noqa: PLC0415

            logger.info("Loading vLLM model: %s", MODEL_NAME)
            _model = LLM(model=MODEL_NAME, task="embed")
            logger.info("Model loaded successfully.")
        except ImportError as exc:
            raise RuntimeError(
                "vLLM is not installed. "
                "Install it with: pip install vllm"
            ) from exc
    return _model


def generate_embeddings(texts: List[str]) -> List[List[float]]:
    """Return one embedding vector per input text using vLLM."""
    model = _get_model()
    outputs = model.embed(texts)
    return [list(output.outputs.embedding) for output in outputs]
