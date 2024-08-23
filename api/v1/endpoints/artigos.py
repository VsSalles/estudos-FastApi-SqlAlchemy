from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from models.faculdade import Artigos as ArtigoModel, Usuarios as UsuarioModel
from schemas.faculdade_schema import ArtigoSchema, ArtigoSchemaPut
from core.deps import get_session, valida_token_jwt
from sqlalchemy.future import select
from typing import List

router = APIRouter()

@router.get('/', response_model=List[ArtigoSchema])
async def get_artigos(session: AsyncSession = Depends(get_session), authorized_user: UsuarioModel = Depends(valida_token_jwt)):
    query = await session.execute(select(ArtigoModel))
    result = query.scalars().unique().all()

    return result

@router.get('/{artigo_id}', response_model=ArtigoSchema)
async def get_artigo(artigo_id: int, session: AsyncSession = Depends(get_session), authorized_user: UsuarioModel = Depends(valida_token_jwt)):
    query = await session.execute(select(ArtigoModel).filter(ArtigoModel.id == artigo_id))
    result = query.scalars().unique().one_or_none()

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'msg': 'Artigo não encontrado'})
    
    return result

@router.post('/', response_model=ArtigoSchema)
async def create_artigo(artigo: ArtigoSchema, session: AsyncSession = Depends(get_session), authorized_user: UsuarioModel = Depends(valida_token_jwt)):
    novo_artigo = ArtigoModel(titulo=artigo.titulo, descricao=artigo.descricao, url_fonte=artigo.url_fonte, id_usuario=authorized_user.id)
    session.add(novo_artigo)
    await session.commit()

    return novo_artigo

@router.put('/{artigo_id}', response_model=ArtigoSchema)
async def update_artigo(artigo_id : int, artigo_up: ArtigoSchemaPut, session: AsyncSession = Depends(get_session), authorized_user: UsuarioModel = Depends(valida_token_jwt)):
    query = await session.execute(select(ArtigoModel).filter(ArtigoModel.id == artigo_id))
    result = query.scalars().unique().one_or_none()

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'msg': 'Artigo não encontrado'})
    
    result.titulo = artigo_up.titulo
    result.descricao = artigo_up.descricao
    result.url_fonte = artigo_up.url_fonte
    
    await session.commit()

    return result

@router.delete('/{artigo_id}')
async def delete_artigo(artigo_id: int, session: AsyncSession = Depends(get_session), authorized_user: UsuarioModel = Depends(valida_token_jwt)):
    query = await session.execute(select(ArtigoModel).filter(ArtigoModel.id == artigo_id))
    result = query.scalars().unique().one_or_none()

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'msg': 'Artigo não encontrado'})
    
    await session.delete(result)
    await session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)