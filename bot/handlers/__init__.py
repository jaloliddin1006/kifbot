"""
Handlers package
"""

from .basic import router as basic_router
from .request import router as request_router
from .admin import router as admin_router

# Barcha routerlarni eksport qilish
routers = [
    request_router,
    admin_router,
    basic_router
]

__all__ = ['routers']
