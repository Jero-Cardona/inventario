import logging
from fastapi import FastAPI, Depends, HTTPException, APIRouter, status, Response, Request, Form
from sqlalchemy.orm import Session, joinedload
from . import crud, models, schemas
from app.schemas import *
from .database import SessionLocal, engine
from starlette.status import *
from typing import List
from datetime import datetime, date
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
# importaciones para utilizar con el Front
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from .router import auth
from app.router.auth import get_user_disabled_current, oauth2_scheme



# Obtener la fecha actual
now = datetime.now()

year = now.year
month = now.month
day = now.day

# Crear un objeto de fecha con los valores actuales
fecha_actual = date(year, month, day)
fecha_creacion = fecha_actual

# App de FastAPI
app = FastAPI()
app.include_router(auth.router)
# Servir archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configurar Jinja2 para usar la carpeta templates
templates = Jinja2Templates(directory="templates")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

models.Base.metadata.create_all(bind=engine)
# responsable = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Añadir middleware de sesiones
app.add_middleware(SessionMiddleware, secret_key="!secret_key!")

@app.get("/inicio", response_class=JSONResponse, tags=['Routes Templates'])
async def inicio_main(request: Request, db: Session = Depends(get_db)):
    productos = db.query(models.Producto).order_by(models.Producto.id.asc())
    return templates.TemplateResponse("inicio.html", {"request": request, "productos": productos})

@app.get("/proveedor-section", response_class=HTMLResponse, tags=['Routes Templates'])
async def proveedor_main(request: Request, db: Session = Depends(get_db), usuario: Usuarios = Depends(get_user_disabled_current)):
    print(usuario.nombre, usuario.id, usuario.correo)
    print(request.session.values())
    if request.session.get('nombre'):
        proveedores = db.query(models.Proveedor).order_by(models.Proveedor.id.asc())
        return templates.TemplateResponse("proveedor.html", {"request": request, "proveedores": proveedores})
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se soluciona el error JAJAJAJ")

# ubicacion dentro de los endpoints de sedes

@app.get("/categorias-section", response_class=HTMLResponse, tags=['Routes Templates'])
async def categorias_main(request: Request, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    categorias = db.query(models.Categoria).order_by(models.Categoria.id.asc())
    return templates.TemplateResponse("categorias.html", {"request": request, "categorias": categorias})

@app.get("/roles-section", response_class=HTMLResponse, tags=['Routes Templates'])
async def roles_main(request: Request, db: Session = Depends(get_db)):
    roles = db.query(models.Roles).order_by(models.Roles.id.asc())
    return templates.TemplateResponse("roles.html", {"request": request, "roles": roles})

@app.get("/reportes-section", response_class=HTMLResponse, tags=['Routes Templates'])
async def reportes_main(request: Request):
    return templates.TemplateResponse("reportes.html", {"request": request})

@app.get("/sede-section", response_class=HTMLResponse, tags=['Routes Templates'])
async def sedes_main(request: Request, db: Session = Depends(get_db)):
    sedes = db.query(models.Sede).order_by(models.Sede.id.asc())
    return templates.TemplateResponse("sede.html", {"request": request, "sedes": sedes})

# endpoint responsable
@app.get("/responsables-section", response_class=HTMLResponse, tags=['Routes Templates'])
async def responsable_main(request: Request, db: Session = Depends(get_db)):
    responsables = db.query(models.Responsable).order_by(models.Responsable.id.asc())
    return templates.TemplateResponse("responsables.html", {"request": request, "responsables": responsables})

@app.post("/crear-Responsable", response_class=HTMLResponse, tags=['Routes Templates'])
async def add_responsable(request: Request, nombre: str = Form(...), correo: str = Form(...), telefono: str = Form(...),
    db: Session = Depends(get_db)):
    responsable = models.Responsable(nombre=nombre, correo=correo, telefono=telefono)
    db.add(responsable)
    db.commit()
    return RedirectResponse(url=app.url_path_for("responsable_main"), status_code=status.HTTP_303_SEE_OTHER)

# ruta principal de los productos
@app.get("/productos-section", response_class=HTMLResponse, tags=['Routes Templates'])
async def productos_main(request: Request, db: Session = Depends(get_db)):
    productos = db.query(models.Producto).options(
        joinedload(models.Producto.responsable),
        joinedload(models.Producto.sede),
        joinedload(models.Producto.categoria),
        joinedload(models.Producto.proveedor)
    ).order_by(models.Producto.id.asc()).all()
    
    # Otros datos necesarios para la plantilla
    responsables = db.query(models.Responsable).all()
    sedes = db.query(models.Sede).all()
    categorias = db.query(models.Categoria).all()
    proveedores = db.query(models.Proveedor).all()

    return templates.TemplateResponse("productos.html", {
        "request": request,
        "productos": productos,
        "responsables": responsables,
        "sedes": sedes,
        "categorias": categorias,
        "proveedores": proveedores
    })

@app.post("/crear-producto", response_class=HTMLResponse, tags=['Routes Templates'])
async def add_producto(request: Request, producto_data: schemas.ProductoCreate = Depends(schemas.ProductoCreate.as_form), 
    db: Session = Depends(get_db)):
    try:
        producto = models.Producto(**producto_data.dict())
        db.add(producto)
        db.commit()
        return RedirectResponse(url=app.url_path_for("productos_main"), status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# rutas o endpoints de los usuarios
@app.get("/usuarios-section", response_class=HTMLResponse, tags=['Routes Templates'])
async def usuarios_main(request: Request, db: Session = Depends(get_db)):
    usuarios = db.query(models.Usuarios).options(joinedload(models.Usuarios.rol)).order_by(models.Usuarios.id.asc())
    roles = db.query(models.Roles).all()
    return templates.TemplateResponse("usuarios.html", {"request": request, "usuarios": usuarios, "roles": roles, "fecha_creacion": fecha_creacion})

@app.get("/mantenimiento-section", response_class=HTMLResponse, tags=['Routes Templates'])
async def mantenimiento_main(request: Request, db: Session = Depends(get_db)):
    mantenimientos = db.query(models.Mantenimiento).options(
        joinedload(models.Mantenimiento.usuario),
        joinedload(models.Mantenimiento.producto)).order_by(models.Mantenimiento.id.asc())
    productos = db.query(models.Producto).all()
    usuarios = db.query(models.Usuarios).all()
    return templates.TemplateResponse("mantenimiento.html", {"request": request, "mantenimientos": mantenimientos, "usuarios": usuarios, "productos": productos})

@app.post("/crear-mantenimiento", response_class=HTMLResponse, tags=['Routes Templates'])
async def add_mantenimiento(request: Request, fecha_mantenimiento: date = Form(...), 
    observacion: str = Form(...), id_usuarios: int = Form(...), id_producto: int = Form(...),
    db: Session = Depends(get_db)):
    mantenimiento = models.Mantenimiento(fecha_mantenimiento=fecha_mantenimiento, 
    observacion=observacion, id_usuarios=id_usuarios, id_producto=id_producto)
    db.add(mantenimiento)
    db.commit()
    return RedirectResponse(url=app.url_path_for("mantenimiento_main"), status_code=status.HTTP_303_SEE_OTHER)

# desde la documentacion de Fastapi

# Create a Responsable
@app.post("/responsable-create/", response_model=schemas.Responsable, tags=['Routes Responsable'])
def create_responsable(responsable: schemas.ResponsableCreate, db: Session = Depends(get_db)):
    return crud.create_responsable(db=db, responsable=responsable)

# Read Responsables
@app.get("/responsables/", response_model=List[schemas.Responsable], tags=['Routes Responsable'])
def read_responsables(db: Session = Depends(get_db)):
    responsables = crud.get_all_responsables(db)
    return responsables

# Read Responsable
@app.get("/responsable/{responsable_id}", response_model=schemas.Responsable, tags=['Routes Responsable'])
def read_responsable(responsable_id: int, db: Session = Depends(get_db)):
    db_responsable = crud.get_responsable(db=db, responsable_id=responsable_id)
    if db_responsable is None:
        raise HTTPException(status_code=404, detail="Responsable not found")
    return db_responsable

# update Responsable
@app.put("/responsable-update/{responsable_id}", response_model=schemas.Responsable, tags=['Routes Responsable'])
def update_responsable(responsable_id: int, nombre: str, correo: str, telefono: str, db: Session = Depends(get_db)):
    try:
        updated_responsable = crud.update_responsable(db, responsable_id, nombre, correo, telefono)
        if not updated_responsable:
            raise HTTPException(status_code=404, detail="No se encontró el responsable")
        return {"message": "Responsable actualizado correctamente", "responsable": updated_responsable}
    except Exception as e:
        logger.error(f"Error al actualizar el responsable: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

# Deleted Responsable
@app.delete("/responsable-deleted/{responsable_id}", response_model=schemas.Responsable, tags=['Routes Responsable'])
def delete_responsable(responsable_id: int, db: Session = Depends(get_db)):
    del_responsable = crud.delete_responsable(db=db, responsable_id=responsable_id)
    if del_responsable == "Deleted Responsable":
        return JSONResponse(content={"detail": "Responsable deleted OK"}, status_code=200)
    elif del_responsable == "ForeignKeyViolation":
        raise HTTPException(status_code=409, detail="Cannot delete responsable, it is referenced by other records")
    else:
        raise HTTPException(status_code=404, detail="Responsable not found")

