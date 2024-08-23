from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from core.database import Session
from core.config import settings
from core.auth import oauth2_schema
from models.faculdade import Usuarios as UsuarioModel
from jose import jwt, JWTError

class TokenData(BaseModel):
    username: Optional[str] = None


async def get_session():
    session: AsyncSession = Session()
    try:
        yield session
    finally:
        await session.close()

async def valida_token_jwt(session: AsyncSession = Depends(get_session), token: str = Depends(oauth2_schema)) -> UsuarioModel:
    '''
    função que valida o tokenJWT e retorna o usuario 
    '''
    credencial_exception: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail={'msg': 'token invalido'}, 
        headers={'WWW-Authenticate':'bearer'}
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.ALGORITHM], options={'verify_aud': False})
        user_id: str = payload.get('sub')

        if user_id is None:
            raise credencial_exception
        
        token_data: TokenData = TokenData(username=user_id)

    except JWTError:
        raise credencial_exception

    query = await session.execute(select(UsuarioModel).filter(UsuarioModel.id == int(token_data.username)))    
    db_user: UsuarioModel = query.scalars().unique().one_or_none()

    if db_user is None:
        raise credencial_exception
    
    return db_user    

