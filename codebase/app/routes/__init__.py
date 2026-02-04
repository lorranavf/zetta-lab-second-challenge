from fastapi import APIRouter

from .home import router as home_router
from .user_routes import router as user_router
from .project_routes import router as project_router
from .task_routes import router as task_router
from .auth import router as auth_router


router = APIRouter()

router.include_router(home_router)
router.include_router(user_router)
router.include_router(project_router)
router.include_router(task_router)
router.include_router(auth_router)

__all__ = ["router"]