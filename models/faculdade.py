from core.config import settings
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship


class Usuarios(settings.DB_BASE):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username = Column(String(50), nullable=False)
    sobrenome = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, index=True, unique=True)
    senha = Column(String(256), nullable=False)
    user_admin = Column(Boolean, default=False)
    artigos = relationship("Artigos", cascade='all,delete-orphan', back_populates='criador', uselist=True, lazy='joined')

class Artigos(settings.DB_BASE):
    __tablename__ = 'artigos'
    id = Column(Integer, primary_key=True ,nullable=False)
    titulo = Column(String(50), nullable=False)
    descricao = Column(String(256), nullable=True)
    url_fonte = Column(String(256), nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuarios.id"))
    criador = relationship("Usuarios", back_populates='artigos', lazy='joined')