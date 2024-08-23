from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from models.faculdade import Usuarios as UsuarioModel, Artigos
from schemas.faculdade_schema import UsuarioSchemaArtigo, UsuarioSchemaBase, UsuarioSchemaPost, UsuarioSchemaUpdatePut, UsuarioLoginSchema
from core.auth import autenticar, cria_token_jwt
from core.security import gerar_hash
from core.deps import get_session, valida_token_jwt
from sqlalchemy.future import select
from typing import List
from sqlalchemy.exc import IntegrityError
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get('/', response_model=List[UsuarioSchemaBase])
async def get_users(session: AsyncSession = Depends(get_session), authorized_user: UsuarioModel = Depends(valida_token_jwt)):
    query = await session.execute(select(UsuarioModel))
    result = query.scalars().unique().all()
    return result

@router.get('/{user_id}/', response_model=UsuarioSchemaArtigo)
async def get_user(user_id: int, session: AsyncSession = Depends(get_session), authorized_user: UsuarioModel = Depends(valida_token_jwt)):
    query = await session.execute(select(UsuarioModel).filter(UsuarioModel.id == user_id))
    result = query.scalars().unique().one_or_none()

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'msg': 'usuario não encontrado'})

    return result

@router.post('/cadastro', response_model=UsuarioSchemaBase)
async def cadastro(usuario: UsuarioSchemaPost, session: AsyncSession = Depends(get_session)):
    usuario = UsuarioModel(username=usuario.username, sobrenome=usuario.sobrenome, email=usuario.email, senha=gerar_hash(usuario.senha))
    try:
        session.add(usuario)
        await session.commit()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='ja existe um usuario com esse e-mail')
    return usuario

@router.post('/login')
async def login(user: UsuarioLoginSchema, session: AsyncSession = Depends(get_session)):
    usuario_autenticado = await autenticar(user.email, user.senha, session)

    if usuario_autenticado == 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'msg': 'e-mail invalido, não existe no banco de dados'})
    elif usuario_autenticado == 2:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'msg': 'senha invalida'})
    
    token = cria_token_jwt(usuario_autenticado.id)

    return JSONResponse(content={'access token': token, 'token_type': 'bearer'})
    

@router.put('/{user_id}/', response_model=UsuarioSchemaBase)
async def uptade_user(user_id: int, user_up: UsuarioSchemaUpdatePut, session: AsyncSession = Depends(get_session), authorized_user: UsuarioModel = Depends(valida_token_jwt)):

    query = await session.execute(select(UsuarioModel).filter(UsuarioModel.id == user_id))
    result = query.scalars().unique().one_or_none()

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'msg': 'usuario não encontrado'})
    
    result.username = user_up.username
    result.sobrenome = user_up.sobrenome
    result.senha = gerar_hash(user_up.senha)

    await session.commit()

    return result    

@router.delete('/{user_id}/')
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session), authorized_user: UsuarioModel = Depends(valida_token_jwt)):
    query = await session.execute(select(UsuarioModel).filter(UsuarioModel.id == user_id))
    result = query.scalars().unique().one_or_none()

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'msg': 'usuario não encontrado'})
    
    await session.delete(result)
    await session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get('/logado')
def logado(authorized_user: UsuarioModel = Depends(valida_token_jwt)):
    return authorized_user 

#authorized_user: UsuarioModel = Depends(valida_token_jwt)