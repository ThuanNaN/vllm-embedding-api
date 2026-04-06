from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.config import API_KEY

_security = HTTPBearer()


def verify_api_key(
    credentials: HTTPAuthorizationCredentials = Security(_security),
) -> str:
    """Validate the Bearer token against the configured API_KEY."""
    if not API_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": {
                    "message": "API_KEY is not configured on the server.",
                    "type": "server_error",
                }
            },
        )
    if credentials.credentials != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": {
                    "message": "Unauthorized",
                    "type": "invalid_request_error",
                }
            },
        )
    return credentials.credentials
