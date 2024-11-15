import qrcode
import zipfile
from io import BytesIO
from typing import List
from fastapi.responses import StreamingResponse
from fastapi import FastAPI, Depends, HTTPException, APIRouter, status, Response, Request, Form, Cookie, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from . import crud, models, schemas, middleware
from .database import SessionLocal, engine
from datetime import datetime, date
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from .router import auth, routes, methods, cargue, exporte
from .middleware import VerifyUserActive, AdminUser

now = datetime.now()
year = now.year
month = now.month
day = now.day

fecha_actual = date(year, month, day)
fecha = fecha_actual

app = FastAPI()
app.include_router(auth.router)
app.include_router(routes.routes)
app.include_router(methods.methods)
app.include_router(cargue.cargue)
app.include_router(exporte.exporte)

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

# endpoint user default bd
@app.post("/crear-user-default", response_model=schemas.Usuarios, tags=["Users"])
async def create_default_user(db: Session = Depends(get_db)):

    admin_role = db.query(models.Roles).filter(models.Roles.id == 1).first()
    if not admin_role:
        # Crear el rol "Administrador" si no existe
        admin_role = models.Roles(id=1, nombre="Administrador")
        db.add(admin_role)
        db.commit()
        db.refresh(admin_role)

    existing_user = crud.get_user_by_username(db, nombre="Usuario Admin")
    if existing_user:
        raise HTTPException(status_code=400, detail="El usuario por defecto ya existe.")

    # Crear el usuario por defecto
    usuario_data = schemas.UsuariosCreate(
        nombre="Usuario Admin",
        correo="admin@example.com",
        hashed_password="12345",
        estado="activo",
        fecha_creacion=date.today(),
        id_rol=admin_role.id
    )
    return crud.create_user(db=db, usuario=usuario_data)

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
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado, no se logro cambiar el estado")

@app.put("/desactivar-usuario/{usuario_id}", tags={"Users"})
async def bloquear_usuario_by_admin(usuario_id: int, db: Session = Depends(get_db)):
    usuario = crud.get_usuario(usuario_id, db)
    if usuario:
        usuario.estado = 'inactivo'
        db.commit()
        db.refresh(usuario)
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado, no se logro cambiar el estado")

@app.get("/salir", response_class=HTMLResponse, tags=["Users"])
async def logout(request: Request):
    request.session.pop('nombre', None)
    request.session.pop('correo', None)
    request.session.pop('rol', None)
    request.session.pop('id', None)
    return RedirectResponse(url="/", status_code=302, headers={
        "set-cookie": "access_token=; Max-Age=0"})

# Modelo para recibir las rutas

@app.post("/configurar-rutas")
async def update_routes(data: schemas.RoutesConfig):
    AdminUser.update_excluded_routes(data.routes)
    return {"message": "Rutas actualizadas correctamente", "routes": AdminUser.excluded_routes}


@app.get("/inicio", response_class=JSONResponse, tags=['Routes Templates'])
async def inicio_main(request: Request, db: Session = Depends(get_db)):
    productos = db.query(models.Producto).all()
    responsables = db.query(models.Responsable).options(joinedload(models.Responsable.productos)).order_by(models.Responsable.id.asc()).all()
    
    productos_categorias = (
        db.query(models.Categoria.nombre, func.count(models.Producto.id).label('productos_count')).join(models.Producto, models.Categoria.id == models.Producto.id_categoria).group_by(models.Categoria.id).order_by(models.Categoria.id.asc()).all()
    )

    depreciaciones = crud.depreciacion_categorias(db)
    
    return templates.TemplateResponse("inicio.html", {"request": request, "responsables": responsables, "productos": productos, "depreciaciones": depreciaciones, "productos_categorias": productos_categorias})


@app.get("/proveedor-section", response_class=HTMLResponse, tags=['Routes Templates'])
async def proveedor_main(request: Request, db: Session = Depends(get_db)):
    
    # consultas necesarias para las vistas
    proveedores = db.query(models.Proveedor).order_by(models.Proveedor.id.asc()).all()
    proveedor_mantenimiento = db.query(models.Proveedormantenimiento).options(joinedload(models.Proveedormantenimiento.proveedor), joinedload(models.Proveedormantenimiento.producto)).order_by(models.Proveedormantenimiento.id.asc()).all()
    
    productos = db.query(models.ProductoProveedores).order_by(models.ProductoProveedores.id_producto).options(joinedload(models.ProductoProveedores.producto)).all()
    proveedor_m_productos = (
        db.query(models.Proveedormantenimiento.id_proveedor, func.count(models.Proveedormantenimiento.id_producto).label('productos_p_count'))
        .join(models.ProductoProveedores, models.Proveedormantenimiento.id_producto == models.ProductoProveedores.id)
        .group_by(models.Proveedormantenimiento.id_proveedor)
        .order_by(models.Proveedormantenimiento.id_proveedor.asc())
        .all()
    )
    
    return templates.TemplateResponse("proveedor.html", {"request": request, "proveedores": proveedores, "proveedor_m_productos": proveedor_m_productos, "mantenimientos_pro": proveedor_mantenimiento, "productos": productos})

@app.get("/categoria-section", response_class=HTMLResponse, tags=['Routes Templates'])
async def categorias_main(request: Request, db: Session = Depends(get_db)):
    categorias = db.query(models.Categoria).order_by(models.Categoria.id.asc()).all()
    return templates.TemplateResponse("categorias.html", {"request": request, "categorias": categorias})

@app.get("/rol-section", response_class=HTMLResponse, tags=['Routes Templates'])
async def roles_main(request: Request, db: Session = Depends(get_db)):
    roles = db.query(models.Roles).order_by(models.Roles.id.asc()).all()
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
    sedes = db.query(models.Sede).order_by(models.Sede.id.asc()).all()
    productos = db.query(models.Producto).order_by(models.Producto.id.asc()).all()

    ubicaciones_productos = (
        db.query(models.Ubicacion.nombre, func.count(models.Ubicacion.id_producto).label('productos_count'))
        .join(models.Producto, models.Ubicacion.id_producto == models.Producto.id)
        .group_by(models.Ubicacion.nombre)
        .order_by(models.Ubicacion.nombre.asc())
        .all()
    )
    ubicaciones = db.query(models.Ubicacion).options(
        joinedload(models.Ubicacion.producto),
        joinedload(models.Ubicacion.sede)
    ).order_by(models.Ubicacion.id.asc()).all()
    return templates.TemplateResponse("sede.html", {
        "request": request,
        "sedes": sedes,
        "ubicaciones_productos": ubicaciones_productos,
        "ubicaciones": ubicaciones,
        "productos": productos,
    })
    

@app.get("/responsable-section", response_class=HTMLResponse, tags=['Routes Templates'])
async def responsable_main(request: Request, db: Session = Depends(get_db)):
        responsables = db.query(models.Responsable).order_by(models.Responsable.id.asc()).all()
        return templates.TemplateResponse("responsables.html", {"request": request, "responsables": responsables})

@app.get("/producto-obtener-qr-section/{producto_id}", response_class=HTMLResponse, tags=['Routes Templates'])
async def producto_section_qr(request: Request, producto_id: int, db: Session = Depends(get_db)):
    producto = crud.get_producto(producto_id, db)
    valor_actual = crud.calcular_valor_actual(producto)
    valor_formateado = f"{valor_actual:,.2f}"

    return templates.TemplateResponse(
        "producto_info.html", 
        {
            "request": request,
            "producto": producto,
            "valor_actual": valor_formateado
        }
    )

@app.get("/producto-section", response_class=HTMLResponse, tags=['Routes Templates'])
async def productos_main(request: Request, db: Session = Depends(get_db)):
    # Consulta de productos con todas las relaciones cargadas
    productos = db.query(models.Producto).options(
        joinedload(models.Producto.responsable),
        joinedload(models.Producto.sede),
        joinedload(models.Producto.categoria),
        joinedload(models.Producto.proveedor)
    ).order_by(models.Producto.id.asc()).all()
    
    # depreciacion por activos
    productos_valor_actual = []
    for producto in productos:
        valor_actual = crud.calcular_valor_actual(producto)
        valor = f"{valor_actual:,.2f}"
        productos_valor_actual.append({
            "producto": producto,
            "valor_actual": valor
        })
        
    # Consulta para contar productos por proveedor
    productos_por_proveedor = (
        db.query(models.Proveedor.nombre, func.count(models.Producto.id).label('producto_count'))
        .join(models.Producto, models.Proveedor.id == models.Producto.id_proveedor)
        .group_by(models.Proveedor.id)
        .order_by(models.Proveedor.id.asc())
        .all()
    )
    
    productos_sin_pro = db.query(models.Producto).where(models.Producto.id_proveedor == None).all()

    # Consultas adicionales
    responsables = db.query(models.Responsable).all()
    sedes = db.query(models.Sede).all()
    categorias = db.query(models.Categoria).all()
    proveedores = db.query(models.Proveedor).all()

    # Pasamos todos los objetos al template
    return templates.TemplateResponse("productos.html", {
        "request": request,
        "productos_v": productos_valor_actual,
        "productos": productos,
        "responsables": responsables,
        "sedes": sedes,
        "categorias": categorias,
        "proveedores": proveedores,
        "productos_por_proveedor": productos_por_proveedor,
        "productos_sin_proveedor": productos_sin_pro,
        "fecha_ingreso": fecha
    })


@app.get("/usuario-section", response_class=HTMLResponse, tags=['Routes Templates'])
async def usuarios_main(request: Request, db: Session = Depends(get_db)):
        usuarios = db.query(models.Usuarios).options(joinedload(models.Usuarios.rol)).order_by(models.Usuarios.id.asc()).all()
        roles = db.query(models.Roles).all()
        return templates.TemplateResponse("usuarios.html", {"request": request, "usuarios": usuarios, "roles": roles, "fecha_creacion": fecha})

@app.get("/mantenimiento-section", response_class=HTMLResponse, tags=['Routes Templates'])
async def mantenimiento_main(request: Request,  db: Session = Depends(get_db)):
    mantenimientos = db.query(models.Mantenimiento).filter(models.Mantenimiento.fecha_mantenimiento > fecha_actual).options(
        joinedload(models.Mantenimiento.usuarios),
        joinedload(models.Mantenimiento.producto)).order_by(models.Mantenimiento.id.asc()).all()
    productos = db.query(models.Producto).all()
    usuarios = db.query(models.Usuarios).all()
    
    return templates.TemplateResponse("mantenimiento.html", {"request": request, "mantenimientos": mantenimientos, "productos": productos, "usuarios": usuarios})


# endpoints para codigos QR de productos
@app.get("/generar-codigoqr-producto/{producto_id}", tags=['QR Code'])
async def generar_qr(producto_id: int, db: Session = Depends(get_db)):
    producto = crud.get_producto_for_qr(producto_id, db)

    # Generar la URL de edición del producto
    url_informacion_producto = f"http://3.144.188.2/producto-obtener-qr-section/{producto.id}"

    qr_image = qrcode.make(url_informacion_producto)
    buf = BytesIO()
    qr_image.save(buf)
    buf.seek(0)

    return StreamingResponse(buf, status_code=200, media_type="image/png")

@app.get('/productos-imagen-qr', tags=['QR Code'])
async def image_qr_producto(request: Request, db: Session = Depends(get_db)):
    productos = crud.get_all_productos_for_qr(db)

    zip_buffer = BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for producto in productos:
            url_informacion_producto = f"http://3.144.188.2/producto-obtener-qr-section/{producto.id}"
            

            qr_image = qrcode.make(url_informacion_producto)
            qr_buffer = BytesIO()
            qr_image.save(qr_buffer)
            qr_buffer.seek(0)

            file_name = f"{producto.codigo}_qr.png"
            zip_file.writestr(file_name, qr_buffer.getvalue())

    zip_buffer.seek(0)

    return StreamingResponse(zip_buffer, media_type="application/zip", headers={
        "Content-Disposition": "attachment; filename=productos-codigos_qr.zip"
    })
    
# methods para historial mantenimiento
@app.get('/producto/{codigo_producto}/historial-mantenimiento', tags=['Historial'])
def get_historial_m(codigo_producto: str, db: Session = Depends(get_db)):
    producto = db.query(models.Producto).filter(models.Producto.codigo == codigo_producto).first()
    
    if not producto:
        raise HTTPException(status_code=404, detail="Codigo de producto no encontrado")

    producto_detalles = {
        "codigo": producto.codigo,
        "estado": producto.estado,
        "fecha_ingreso": producto.fecha_ingreso,
        "cantidad": producto.cantidad,
        "responsable": producto.responsable.nombre if producto.responsable else "No asignado",
        "sede": producto.sede.nombre if producto.sede else "No asignada",
        "categoria": producto.categoria.nombre if producto.categoria else "No asignada",
        "proveedor": producto.proveedor.nombre if producto.proveedor else "No asignado"
    }
    
    # Obtener el historial de mantenimientos
    historial_mantenimiento = (
        db.query(models.Mantenimiento)
        .filter(models.Mantenimiento.id_producto == producto.id)
        .all()
    )
    
    historial_detalles = []
    for mantenimiento in historial_mantenimiento:
        proveedor_mantenimiento = db.query(models.Proveedormantenimiento).filter(
            models.Proveedormantenimiento.id_producto == producto.id
        ).first()
        
        historial_detalles.append({
            "fecha_mantenimiento": mantenimiento.fecha_mantenimiento,
            "observacion": mantenimiento.observacion,
            "usuario_responsable": mantenimiento.usuarios.nombre if mantenimiento.usuarios else "Desconocido",
            "proveedor_mantenimiento": proveedor_mantenimiento.proveedor.nombre if proveedor_mantenimiento else "No asignado",
            "contacto_proveedor": proveedor_mantenimiento.contacto if proveedor_mantenimiento else "No contactos de proveedores"
        })

    historial = {
        "producto": producto_detalles,
        "historial_mantenimiento": historial_detalles
    }

    if not historial["historial_mantenimiento"]:
        raise HTTPException(status_code=400, detail="No hay mantenimientos relacionados a este producto")

    return historial