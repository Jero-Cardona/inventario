from fastapi import FastAPI, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import SessionLocal, engine
from .. import schemas, models, crud, security
from app.schemas import *
from ..security import *

models.Base.metadata.create_all(bind=engine)
routes = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@routes.get("/responsable-obtener/{responsable_id}", response_model=schemas.Responsable, tags=['Routes get record'])
def obtener_responsable(responsable_id: int, db: Session = Depends(get_db)):
        return crud.get_responsable(responsable_id, db)

@routes.get("/usuario-obtener/{usuario_id}", response_model=schemas.Usuarios, tags=['Routes get record'])
def obtener_user(usuario_id: int, db: Session = Depends(get_db)):
        return crud.get_usuario(usuario_id, db)

@routes.get("/producto-obtener/{producto_id}", response_model=schemas.Producto, tags=['Routes get record'])
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
        return crud.get_producto(producto_id, db)

@routes.get("/proveedor-obtener/{proveedor_id}", response_model=schemas.Proveedor, tags=['Routes get record'])
def obtener_proveedor(proveedor_id: int, db: Session = Depends(get_db)):
        return crud.get_proveedor(proveedor_id, db)

@routes.get("/sede-obtener/{sede_id}", response_model=schemas.Sede, tags=['Routes get record'])
def obtener_sede(sede_id: int, db: Session = Depends(get_db)):
        return crud.get_sede(sede_id, db)

@routes.get("/categoria-obtener/{categoria_id}", response_model=schemas.Categoria, tags=['Routes get record'])
def obtener_categoria(categoria_id: int, db: Session = Depends(get_db)):
        return crud.get_categoria(categoria_id, db)

@routes.get("/mantenimiento-obtener/{mantenimiento_id}", response_model=schemas.Mantenimiento, tags=['Routes get record'])
def obtener_mantenimiento(mantenimiento_id: int, db: Session = Depends(get_db)):
        return crud.get_mantenimiento(mantenimiento_id, db)

@routes.get("/rol-obtener/{rol_id}", response_model=schemas.Roles, tags=['Routes get record'])
def obtener_rol(rol_id: int, db: Session = Depends(get_db)):
        return crud.get_rol(rol_id, db)

# endpoints obtener todos los registros

@routes.get("/responsables-all/", tags=['Routes get all'])
def responsables_all(db: Session = Depends(get_db)):
        return crud.get_all_responsables(db)

@routes.get("/productos-all/", tags=['Routes get all'])
def productos_all(db: Session = Depends(get_db)):
        return crud.get_all_productos(db)

@routes.get("/usuarios-all/", tags=['Routes get all'])
def usuarios_all(db: Session = Depends(get_db)):
        return crud.get_all_usuarios(db)

@routes.get("/categorias-all/", tags=['Routes get all'])
def categorias_all(db: Session = Depends(get_db)):
        return crud.get_all_categorias(db)

@routes.get("/sedes-all/", tags=['Routes get all'])
def sede_all(db: Session = Depends(get_db)):
        return crud.get_all_sedes(db)

@routes.get("/proveedores-all/", tags=['Routes get all'])
def sede_all(db: Session = Depends(get_db)):
        return crud.get_all_proveedores(db)

@routes.get("/roles-all/", tags=['Routes get all'])
def roles_all(db: Session = Depends(get_db)):
        return crud.get_all_roles(db)

@routes.get("/mantenimientos-all/", tags=['Routes get all'])
def mantenimientos_all(db: Session = Depends(get_db)):
        return crud.get_all_mantenimientos(db)