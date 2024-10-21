from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote

# contraseña de postgresql
password = "12345" # Contraseña con un espacio
database_name = "inventario"
# Crea la URL de conexión usando la contraseña codificada
SQLALCHEMY_DATABASE_URL = f"postgresql://jeronimo:{password}@db:5432/{database_name}"
# Configuración de SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=20, max_overflow=40, pool_recycle = 3600)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
