from pydantic import BaseConfig
from sqlalchemy.orm import declarative_base

class Settings(BaseConfig):
    '''conf gerais da aplicação'''
    API_VERSION: str = '/api/v1'
    DB_URL: str = 'postgresql+asyncpg://postgres:Inovepg123@localhost:5433/faculdade'
    DB_BASE = declarative_base()

    #import secrets token = secrets.token_urlsafe(32)    
    JWT_SECRET: str = '6GmTLVPtx3VYdQNRrE-AENcTs7oFH-RFkIugMDShn6w'
    ALGORITHM: str = 'HS256'

    #60 minutos * 24 horas * 7 dias = 1 semana
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    
    class Config:
        case_sensitive = True


settings: Settings = Settings()
