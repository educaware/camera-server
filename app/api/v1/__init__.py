from fastapi import APIRouter

from app.api.v1 import clients, ws

api_router = APIRouter()

# Include routers.
api_router.include_router(ws.router, prefix="/ws")
api_router.include_router(clients.router, prefix="/clients")
