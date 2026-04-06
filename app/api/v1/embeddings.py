import logging
from typing import List

from fastapi import APIRouter, Depends

from app.dependencies import verify_api_key
from app.schemas.embeddings import (
    EmbeddingData,
    EmbeddingRequest,
    EmbeddingResponse,
    EmbeddingUsage,
)
from app.services.embedding_service import generate_embeddings
from app.utils.tokens import count_tokens

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/embeddings", response_model=EmbeddingResponse)
async def create_embeddings(
    request: EmbeddingRequest,
    _: str = Depends(verify_api_key),
) -> EmbeddingResponse:
    """Generate embeddings for the provided input texts (OpenAI-compatible)."""
    texts: List[str] = (
        [request.input] if isinstance(request.input, str) else list(request.input)
    )

    vectors = generate_embeddings(texts)

    total_tokens = sum(count_tokens(t) for t in texts)

    data = [
        EmbeddingData(object="embedding", embedding=vec, index=idx)
        for idx, vec in enumerate(vectors)
    ]

    return EmbeddingResponse(
        object="list",
        data=data,
        model=request.model,
        usage=EmbeddingUsage(
            prompt_tokens=total_tokens,
            total_tokens=total_tokens,
        ),
    )
