from fastapi import APIRouter
from app.api.endpoints import learn, operate, create

api_router = APIRouter()
api_router.include_router(learn.router, prefix="/learn", tags=["learn"])
api_router.include_router(operate.router, prefix="/operate", tags=["operate"])
api_router.include_router(create.router, prefix="/create", tags=["create"])
