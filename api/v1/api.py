from api.v1.endpoints import artigos 
from api.v1.endpoints import usuarios 
from fastapi import APIRouter

api_router= APIRouter()

api_router.include_router(artigos.router, prefix='/artigos', tags=['artigos'])
api_router.include_router(usuarios.router, prefix='/usuarios', tags=['usuarios'])
