from fastapi import APIRouter
from app.api.v1.routes import items_router, products_router, files_router, users_router

router = APIRouter(prefix="/api/v1", tags=["v1"])

router.include_router(items_router)
router.include_router(products_router)
router.include_router(files_router)
router.include_router(users_router)
