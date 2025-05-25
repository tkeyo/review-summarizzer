from fastapi import APIRouter

router = APIRouter()

@router.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    """Health check endpoint to verify the service is alive.

    Returns:
        dict[str, str]: Service status.
    """
    return {"status": "ok"} 