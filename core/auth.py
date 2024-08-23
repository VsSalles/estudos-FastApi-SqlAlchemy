from pytz import timezone
from typing import Optional, List
from datetime import timedelta, datetime
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt
from models.faculdade import Usuarios as UsuarioModel
from core.config import settings
from core.security import verificar_senha
from pydantic import EmailStr

oauth2_schema = OAuth2PasswordBearer(
    tokenUrl=settings.API_VERSION + '/usuarios/login'
)

async def autenticar(email: EmailStr, senha: str, session: AsyncSession) -> Optional[UsuarioModel]:
    '''
    função que autentica o usuario, primeiro busca no banco o usuario com o email informado
    se existir valida se a senha informada esta correta, com base na hash salva no banco
    '''
    query = await session.execute(select(UsuarioModel).filter(UsuarioModel.email == email))
    user: UsuarioModel = query.scalars().unique().one_or_none()

    if user is None:
        return 1 #não existe usuario cadastrado com o email informado 
    
    if not verificar_senha(senha, user.senha):
        return 2 # senha invalida
    
    return user


def _cria_token_jwt(tipo_token: str, tempo_vida: timedelta, user_id: int):
    '''função INTERNA que cria o token JWT'''
    payload = {}
    tz_sp = timezone('America/Sao_Paulo')
    expira = datetime.now(tz=tz_sp) + tempo_vida

    payload['type'] = tipo_token
    payload['exp'] = expira
    payload['iat'] = datetime.now(tz=tz_sp)
    payload['sub'] = str(user_id)

     

    return jwt.encode(payload, settings.JWT_SECRET, settings.ALGORITHM) 
    

def cria_token_jwt(user: str) -> str:
    return _cria_token_jwt('access_token', timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES), user)

