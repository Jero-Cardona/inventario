import qrcode
from io import BytesIO
from fastapi.responses import StreamingResponse
from fastapi import FastAPI, Depends, HTTPException, APIRouter, status, Response, Request, Form, Cookie, Query
from sqlalchemy.orm import Session, joinedload
from . import crud, models, schemas, middleware
from app.schemas import *
from .database import SessionLocal, engine
from starlette.status import *
from typing import List, Annotated
from datetime import datetime, date
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from .router import auth, routes, methods, cargue
from .security import *
from .middleware import VerifyUserActive, AdminUser
from jose import jwt, JWTError

now = datetime.now()
year = now.year
month = now.month
day = now.day

fecha_actual = date(year, month, day)
fecha_creacion = fecha_actual

app = FastAPI()
app.include_router(auth.router)
app.include_router(routes.routes)
app.include_router(methods.methods)
app.include_router(cargue.cargue)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

login = RedirectResponse(url="/", status_code=302)
app.add_middleware(SessionMiddleware, secret_key="!secret_key!")
app.add_middleware(VerifyUserActive)
app.add_middleware(AdminUser)

@app.post("/bloquear-usuario", tags=["Users"])
async def bloquear_usuario(username: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, nombre=username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado, no fue posible bloquearlo")
    user.estado = 'inactivo'
    db.commit()  
    db.refresh(user)  
    return user  

@app.put("/activar-usuario/{usuario_id}", tags={"Users"})
async def desbloquear_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = crud.get_usuario(usuario_id, db)
    if usuario:
        usuario.estado = 'activo'
        db.commit()
        db.refresh(usuario)
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado, no se logo cambiar el estado")

@app.put("/desactivar-usuario/{usuario_id}", tags={"Users"})
async def bloquear_usuario_by_admin(usuario_id: int, db: Session = Depends(get_db)):
    usuario = crud.get_usuario(usuario_id, db)
    if usuario:
        usuario.estado = 'inactivo'
        db.commit()
        db.refresh(usuario)
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado, no se logo cambiar el estado")

@app.get("/salir", response_class=HTMLResponse, tags=["Users"])
async def logout(request: Request):
    request.session.pop('nombre', None)
    request.session.pop('correo', None)
    request.session.pop('rol', None)
    return RedirectResponse(url="/", status_code=302, headers={
        "set-cookie": "access_token=; Max-Age=0"})

@app.get("/inicio", response_class=JSONResponse, tags=['Routes Templates'])
async def inicio_main(request: Request, db: Session = Depends(get_db)):
    productos = db.query(models.Producto).all()
    responsables = db.query(models.Responsable).options(joinedload(models.Responsable.productos)).order_by(models.Responsable.id.asc()).all()
    return templates.TemplateResponse("inicio.html", {"request": request, "responsables": responsables, "productos": productos})


@app.get("/proveedor-section", response_class=HTMLResponse, tags=['Routes Templates'])
async def proveedor_main(request: Request, db: Session = Depends(get_db)):
        proveedores = db.query(models.Proveedor).order_by(models.Proveedor.id.asc())
        return templates.TemplateResponse("proveedor.html", {"request": request, "proveedores": proveedores})

@app.get("/categoria-section", response_class=HTMLResponse, tags=['Routes Templates'])
async def categorias_main(request: Request, db: Session = Depends(get_db)):
        categorias = db.query(models.Categoria).order_by(models.Categoria.id.asc())
        return templates.TemplateResponse("categorias.html", {"request": request, "categorias": categorias})

@app.get("/rol-section", response_class=HTMLResponse, tags=['Routes Templates'])
async def roles_main(request: Request, db: Session = Depends(get_db)):
    roles = db.query(models.Roles).order_by(models.Roles.id.asc())
    return templates.TemplateResponse("roles.html", {
            "request": request,
            "roles": roles,
            "id_rol": request.state.id_rol  
        })

@app.get("/reportes-section", response_class=HTMLResponse, tags=['Routes Templates'])
async def reportes_main(request: Request, db: Session = Depends(get_db)):
        return templates.TemplateResponse("reportes.html", {"request": request})

@app.get("/sede-section", response_class=HTMLResponse, tags=['Routes Templates'])
async def sedes_main(request: Request, db: Session = Depends(get_db)):
        sedes = db.query(models.Sede).order_by(models.Sede.id.asc())
        return templates.TemplateResponse("sede.html", {"request": request, "sedes": sedes})

@app.get("/responsable-section", response_class=HTMLResponse, tags=['Routes Templates'])
async def responsable_main(request: Request, db: Session = Depends(get_db)):
        responsables = db.query(models.Responsable).order_by(models.Responsable.id.asc())
        return templates.TemplateResponse("responsables.html", {"request": request, "responsables": responsables})

@app.get("/producto-section", response_class=HTMLResponse, tags=['Routes Templates'])
async def productos_main(request: Request, db: Session = Depends(get_db)):
        productos = db.query(models.Producto).options(
            joinedload(models.Producto.responsable),
            joinedload(models.Producto.sede),
            joinedload(models.Producto.categoria),
            joinedload(models.Producto.proveedor)
        ).order_by(models.Producto.id.asc()).all()
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
            "proveedores": proveedores,
            "fecha_ingreso": fecha_creacion
        })

@app.get("/usuario-section", response_class=HTMLResponse, tags=['Routes Templates'])
async def usuarios_main(request: Request, db: Session = Depends(get_db)):
        usuarios = db.query(models.Usuarios).options(joinedload(models.Usuarios.rol)).order_by(models.Usuarios.id.asc())
        roles = db.query(models.Roles).all()
        return templates.TemplateResponse("usuarios.html", {"request": request, "usuarios": usuarios, "roles": roles, "fecha_creacion": fecha_creacion})

@app.get("/mantenimiento-section", response_class=HTMLResponse, tags=['Routes Templates'])
async def mantenimiento_main(request: Request, access_token: Annotated[str | None, Cookie()] = None, db: Session = Depends(get_db)):
    if access_token is None:
        return login
    try:
        data_user = jwt.decode(access_token, key = SECRET_KEY, algorithms = ALGORITHM)
        mantenimientos = db.query(models.Mantenimiento).options(
            joinedload(models.Mantenimiento.usuarios),
            joinedload(models.Mantenimiento.producto)).order_by(models.Mantenimiento.id.asc())
        productos = db.query(models.Producto).all()
        usuarios = db.query(models.Usuarios).all()
        return templates.TemplateResponse("mantenimiento.html", {"request": request, "mantenimientos": mantenimientos, "usuarios": usuarios, "productos": productos})
    except JWTError:
        return login


@app.get("/generar-codigoqr-producto/{producto_id}", tags=['QR Code'])
async def generar_qr(producto_id: int,  db: Session = Depends(get_db)):
    producto = crud.get_producto_for_qr(producto_id, db)
    
    # informacion del producto en un string
    producto_info = (
        f"ID: {producto.id}\n"
        f"Lider Acargo: {producto.responsable.nombre}\n"
        f"Codigo producto: {producto.codigo}\n"
        f"Sede: {producto.sede.nombre}\n"
        f"Cantidad: {producto.cantidad}\n"
        f"Uso: {producto.uso}\n"
        f"Estado: {producto.estado}\n"
        f"Fecha proximo mantenimiento: {producto.fecha_mantenimiento}\n"
        f"Costo: {producto.costo_inicial}\n"
        f"Modo: {producto.modo}\n"
        f"Observacion: {producto.observacion}\n"
        f"Categoria: {producto.categoria.nombre}\n"
        f"Proveedor: {producto.proveedor.nombre}\n"
        f"Ingreso: {producto.fecha_ingreso}"
    )
    
    # Generar la imagen del QR
    qr_image = qrcode.make(producto_info)
    buf = BytesIO()
    qr_image.save(buf)
    buf.seek(0)
    
    return StreamingResponse(buf, status_code=200, media_type="image/png")

@app.get('imagen-qr', tags=['QR Code'])
async def image_qr_producto(request: Request, db: Session = Depends(get_db)):
    a = 22