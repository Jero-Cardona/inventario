from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus

# contraseña de postgresql
password = " " # Contraseña con un espacio
database_name = "inventario"
# Crea la URL de conexión usando la contraseña codificada
SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:{password}@localhost:5432/{database_name}"
# Configuración de SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
