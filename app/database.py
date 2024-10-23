from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config.config import Settings

setting = Settings()

POSTGRES_USER = setting.postgres_user
POSTGRES_PASSWORD = setting.postgres_password 
POSTGRES_DB = setting.postgres_db
POSTGRES_HOST = setting.postgres_host
POSTGRES_PORT = setting.postgres_port

# Crea la URL de conexión usando la contraseña codificada
DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(DATABASE_URL, echo= True, pool_size=20, max_overflow=40, pool_recycle = 3600)
SessionLocal = sessionmaker(bind = engine)
Base = declarative_base()
