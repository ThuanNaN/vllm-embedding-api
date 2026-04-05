from fastapi import APIRouter, Depends

from app.config import MODEL_NAME
from app.dependencies import verify_api_key
from app.schemas.models import ModelInfo, ModelsResponse

router = APIRouter()


@router.get("/models", response_model=ModelsResponse)
async def list_models(
    _: str = Depends(verify_api_key),
) -> ModelsResponse:
    """Return the list of available models (OpenAI-compatible)."""
    return ModelsResponse(
        object="list",
        data=[
            ModelInfo(
                id=MODEL_NAME,
                object="model",
                owned_by="local",
            )
        ],
    )
