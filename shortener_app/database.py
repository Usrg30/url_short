from sqlite3 import connect
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from . config import get_settings

engine = create_engine(
    get_settings().db_url, connect_args={"check_same_thread": False}
) # punto de entradad e la base de datos e instancia la engine

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)   # instancia la sesionmaker

Base = declarative_base()  # instancia la base, conecta el motor de la base de datos con la sqlalchemy
