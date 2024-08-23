from pydantic import BaseModel, EmailStr, HttpUrl
from typing import List, Optional

class ArtigoSchema(BaseModel):
    id: Optional[int] = None
    titulo: str
    descricao: str
    url_fonte: str
    id_usuario: Optional[int] = None

    class Config:
        from_attributes = True

class ArtigoSchemaPut(BaseModel):
    titulo: str
    descricao: str
    url_fonte: str

    class Config:
        from_attributes = True



class UsuarioSchemaBase(BaseModel):
    id: Optional[int] = None
    username: str
    sobrenome: str
    email: EmailStr
    user_admin: Optional[bool] = False

    class Config:
        from_attributes = True

class UsuarioSchemaPost(UsuarioSchemaBase):
    senha: str

class UsuarioSchemaUpdateParcial(UsuarioSchemaBase):
    username: Optional[str]
    sobrenome: Optional[str]
    email: Optional[EmailStr]
    senha: Optional[str]
    user_admin: Optional[bool]

class UsuarioSchemaUpdatePut(BaseModel):
    username: str
    sobrenome: str
    senha: str

    class Config:
        from_attributes = True

class UsuarioSchemaArtigo(UsuarioSchemaBase):
    artigos: Optional[List[ArtigoSchema]]

class UsuarioLoginSchema(BaseModel):
    email: EmailStr
    senha: str

    class Config:
        from_attributes = True



