from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped


class Base(DeclarativeBase):
    pass


class BaseModels:
    id = Column(Integer, primary_key=True, autoincrement=True)
    date_in = Column(DateTime, default=datetime.now(timezone.utc))
    status = Column(Boolean, default=True)


class Produtos(Base, BaseModels):
    __tablename__ = 'produtos'

    name = Column(String)
    ean = Column(Integer)
    value = Column(Float, default=0)


class ScrapedProdutos(Base, BaseModels):
    __tablename__ = 'scraped_produtos'

    seller = Column(String)
    name = Column(String)
    ean = Column(Integer)
    value = Column(Float, default=0)
