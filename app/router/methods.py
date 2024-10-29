from fastapi import FastAPI, Depends, HTTPException, APIRouter, status, Response, Request, Form, Cookie, Query
from sqlalchemy.orm import Session, joinedload
from .. import crud, models, schemas
from app.schemas import *
from ..security import *
from ..database import SessionLocal, engine
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from typing import List, Optional

models.Base.metadata.create_all(bind=engine)
methods = APIRouter()

now = datetime.now()
year = now.year
month = now.month
day = now.day

fecha_actual = date(year, month, day)
fecha_creacion = fecha_actual

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@methods.post("/crear-mantenimiento", response_class=HTMLResponse, tags=['Routes Post'])
async def add_mantenimiento(request: Request, fecha_mantenimiento: date = Form(...), 
    observacion: str = Form(...), id_usuarios: int = Form(...), id_producto: int = Form(...),
    db: Session = Depends(get_db)):
    mantenimiento = models.Mantenimiento(fecha_mantenimiento=fecha_mantenimiento, 
    observacion=observacion, id_usuarios=id_usuarios, id_producto=id_producto)
    db.add(mantenimiento)
    db.commit()
    return RedirectResponse(url="/mantenimiento-section", status_code=status.HTTP_303_SEE_OTHER)

@methods.post("/crear-rol", response_class=HTMLResponse, tags=['Routes Post'])
async def add_rol(request: Request, nombre: str = Form(...), db: Session = Depends(get_db)):
    rol = models.Roles(nombre=nombre)
    db.add(rol)
    db.commit()
    return RedirectResponse(url="/rol-section", status_code=status.HTTP_303_SEE_OTHER)

@methods.post("/crear-sede", response_class=HTMLResponse, tags=['Routes Post'])
async def add_sede(request: Request, nombre: str = Form(...), direccion :str = Form(...), 
    telefono: str = Form(...), db: Session = Depends(get_db)):
    sede = models.Sede(nombre=nombre, direccion=direccion, telefono=telefono)
    db.add(sede)
    db.commit()
    return RedirectResponse(url="/sede-section", status_code=status.HTTP_303_SEE_OTHER)

@methods.post("/crear-proveedor", response_class=HTMLResponse, tags=['Routes Post'])
async def add_proveedores(request: Request, nombre: str = Form(...), direccion: str = Form(...), 
    telefono: str = Form(...), db: Session = Depends(get_db)):
    proveedor = models.Proveedor(nombre=nombre, direccion=direccion, telefono=telefono)
    db.add(proveedor)
    db.commit()
    return RedirectResponse(url="/proveedor-section", status_code=status.HTTP_303_SEE_OTHER)

@methods.post("/crear-categoria", response_class=HTMLResponse, tags=['Routes Post'])
async def add_categoria(request: Request, nombre: str = Form(...), depreciacion: float = Form(...), db: Session = Depends(get_db)):
    categoria = models.Categoria(nombre=nombre, depreciacion=depreciacion)
    db.add(categoria)
    db.commit()
    return RedirectResponse(url="/categoria-section", status_code=status.HTTP_303_SEE_OTHER)

@methods.post("/crear-producto", response_class=HTMLResponse, tags=['Routes Post'])
async def add_producto(request: Request, producto_data: schemas.ProductoCreate = Depends(schemas.ProductoCreate.as_form), 
    db: Session = Depends(get_db)):
    try:
        verify_cod_producto = crud.get_cod_producto(db, codigo = producto_data.codigo)
        if verify_cod_producto:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = "Este codigo ya existe, por favor intenta otro")
        producto = models.Producto(**producto_data.dict(exclude_unset=True))
        db.add(producto)
        db.commit()

        # si el producto cuenta con proveedor instanciar en otro modelo
        if producto_data.id_proveedor is not None:
            producto_proveeores = models.ProductoProveedores(
                id_producto = producto.id,
                id_proveedor = producto_data.id_proveedor
            )
            db.add(producto_proveeores)
            db.commit()
        
        return RedirectResponse(url="/producto-section", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@methods.post("/crear-Responsable", response_class=HTMLResponse, tags=['Routes Post'])
async def add_responsable(request: Request, nombre: str = Form(...), correo: str = Form(...), telefono: str = Form(...),
    db: Session = Depends(get_db)):
    responsable = models.Responsable(nombre=nombre, correo=correo, telefono=telefono)
    db.add(responsable)
    db.commit()
    return RedirectResponse(url="responsable-section", status_code=status.HTTP_303_SEE_OTHER)

@methods.post("/crear-proveedor-mantenimiento", response_class=HTMLResponse, tags=['Routes Post'])
async def crear_proveedormantenimiento(
    id_proveedor: int = Form(...), 
    contacto: str = Form(...), 
    id_producto: int = Form(...), 
    db: Session = Depends(get_db)
):
    proveedor_mantenimimiento = models.Proveedormantenimiento(
        contacto = contacto,
        id_producto = id_producto,
        id_proveedor = id_proveedor
    )
    db.add(proveedor_mantenimimiento)
    db.commit()
    return RedirectResponse(url="/proveedor-section", status_code=status.HTTP_303_SEE_OTHER)

@methods.post("/crear-ubicacion-producto", response_class=HTMLResponse, tags=['Routes Post'])
async def add_ubicacion(
    nombre: str = Form(...),
    id_sede: int = Form(...),
    id_producto: int = Form(...),
    db: Session = Depends(get_db)
):
    Ubicacion = models.Ubicacion(
        nombre = nombre,
        id_sede = id_sede,
        id_producto = id_producto
    )
    db.add(Ubicacion)
    db.commit()
    return RedirectResponse(url="/sede-section", status_code=status.HTTP_303_SEE_OTHER)

@methods.post("/crear-proveedor-mantenimiento", response_class=HTMLResponse, tags=['Routes Post'])
async def add_ubicacion(
    contacto: str = Form(...),
    id_proveedor: int = Form(...),
    id_producto: int = Form(...),
    db: Session = Depends(get_db)
):
    provedor = models.Proveedormantenimiento(
        contacto = contacto,
        id_proveedor = id_proveedor,
        id_producto = id_producto
    )
    db.add(provedor)
    db.commit()
    return RedirectResponse(url="/proveedor-section", status_code=status.HTTP_303_SEE_OTHER)

# Endpoints con el metodo PUT

@methods.put("/proveedor-update/{proveedor_id}", response_model=schemas.Proveedor, tags=['Routes Put'])
def update_proveedor(proveedor_id: int, nombre: str, direccion: str, telefono: str, db: Session = Depends(get_db)):
    try:
        updated_proveedor_id = crud.update_proveedor(db, proveedor_id, nombre, direccion, telefono)
        if not updated_proveedor_id:
            raise HTTPException(status_code=404, detail="No se encontró el proveedor")
        return updated_proveedor_id
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@methods.put("/producto-update/{producto_id}", response_model=schemas.Producto, tags=['Routes Put'])
def update_pro(producto_id: int, id_responsable: int, codigo: str, id_sede: int, cantidad: int, uso: str, 
            estado: str, fecha_mantenimiento: date, costo_inicial: float, modo: str, observacion: str,
            id_categoria: int, fecha_ingreso: date, db: Session = Depends(get_db), id_proveedor: Optional[int] = None):
    try:
        existing_producto = crud.get_cod_producto(db, codigo=codigo)
        
        if existing_producto and existing_producto.id != producto_id:
            raise HTTPException(status_code=400, detail="Este código ya existe, por favor intenta otro")

        update_producto_id = crud.update_producto(db, producto_id, id_responsable, codigo, id_sede,
                                                cantidad, uso, estado, fecha_mantenimiento, costo_inicial, modo,
                                                observacion, id_categoria, fecha_ingreso, id_proveedor)
        
        if not update_producto_id:
            raise HTTPException(status_code=404, detail="No se encontró el producto")
        return update_producto_id
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@methods.put("/mantenimiento-update/{mantenimiento_id}", response_model=schemas.Mantenimiento, tags=['Routes Put'])
def update_mantenimiento(mantenimiento_id: int, fecha_mantenimiento: date, observacion: str, id_usuarios: int, id_producto: int,  db: Session = Depends(get_db)):
    try:
        update_mante_id = crud.update_m(db, mantenimiento_id, fecha_mantenimiento, observacion, id_usuarios, id_producto)
        if not update_mante_id:
            raise HTTPException(status_code=404, detail="No se encontró el Mantenimiento")
        return update_mante_id
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@methods.put("/responsable-update/{responsable_id}", response_model=schemas.Responsable, tags=['Routes Put'])
def update_responsable_id(responsable_id: int, nombre: str, correo: str, telefono: str, db: Session = Depends(get_db)):
    try:
        updated_responsable = crud.update_responsable(db, responsable_id, nombre, correo, telefono)
        if not updated_responsable:
            raise HTTPException(status_code=404, detail="No se encontró el responsable")
        return updated_responsable 
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@methods.put("/sede-update/{sede_id}", response_model=schemas.Sede, tags=['Routes Put'])
def update_sede_id(sede_id: int, nombre: str, direccion: str, telefono: str, db: Session = Depends(get_db)):
    try:
        update_sede = crud.update_sede(db, sede_id, nombre, direccion, telefono)
        if not update_sede:
            raise HTTPException(status_code=404, detail="No se encontró la sede")
        return update_sede 
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@methods.put("/ubicacion-update/{ubicacion_id}", response_model=schemas.Ubicacion, tags=['Routes Put'])
def update_ubicacion(ubicacion_id: int, nombre: str, id_sede: int, id_producto: int, db: Session = Depends(get_db)):
    try:
        update_ubi = crud.update_ubication(db, ubicacion_id, nombre, id_sede, id_producto)
        if not update_ubi:
            raise HTTPException(status_code=404, detail="No se encontro la ubicacion")
        return update_ubi
    except Exception as e:
        raise HTTPException(status_code=500, detail='Error interno del servidor')

@methods.put("/rol-update/{rol_id}", response_model=schemas.Roles, tags=['Routes Put'])
def update_rol_id(rol_id: int, nombre: str, db: Session = Depends(get_db)):
    try:
        update_rol = crud.update_rol(db, rol_id, nombre)
        if not update_rol:
            raise HTTPException(status_code=404, detail="No se encontró el Rol")
        return update_rol 
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@methods.put("/categoria-update/{categoria_id}", response_model=schemas.Categoria, tags=['Routes Put'])
def update_categoria_id(categoria_id: int, nombre: str, depreciacion: float, db: Session = Depends(get_db)):
    try:
        update_categoria_id = crud.update_categoria(db, categoria_id, nombre, depreciacion)
        if not update_categoria_id:
            raise HTTPException(status_code=404, detail="No se encontró la Categoria")
        return update_categoria_id 
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@methods.put("/usuario-update/{usuario_id}", response_model=schemas.Usuarios, tags=['Routes Put'])
def update_usuario(
    usuario_id: int,
    nombre: str, correo: str, hashed_password: str, estado: str,
    fecha_creacion: date, id_rol: int,
    db: Session = Depends(get_db)
):
    db_user = crud.get_user_by_id(db, usuario_id=usuario_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db_user_with_same_name = crud.get_user_by_username(db, nombre=nombre)
    if db_user_with_same_name and db_user_with_same_name.id != usuario_id:
        raise HTTPException(status_code=400, detail="Este nombre de usuario ya fue registrado")

    return crud.update_user(db=db, usuario_id=usuario_id, nombre=nombre, correo=correo,
                            hashed_password=hashed_password, estado=estado, fecha_creacion=fecha_creacion, id_rol=id_rol)

@methods.put("/proveedor_mante-update/{proveedor_mante_id}", response_model=schemas.ProveedorMantenimiento, tags=['Routes Put'])
def update_provedor_mantenimiento(
    proveedor_mante_id: int, 
    contacto: str, id_proveedor: int, id_producto: int,
    db: Session = Depends(get_db)
):
    try:
        db_proveedor_m = crud.update_proveedor_m(db, proveedor_mante_id, contacto, id_proveedor, id_producto)
        if not db_proveedor_m:
            raise HTTPException(status_code=404, detail="Registro no encontrado")
        return db_proveedor_m
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"error {e}, problemas con el servidor")

# methods delete for records
@methods.delete("/responsable-deleted/{responsable_id}", response_model=schemas.Responsable, tags=['Routes Delete'])
def delete_responsable(responsable_id: int, db: Session = Depends(get_db)):
    del_responsable = crud.delete_responsable(db = db, responsable_id = responsable_id)
    if del_responsable == "Deleted Responsable":
        return JSONResponse(content={"detail": "Responsable deleted OK"}, status_code=200)
    elif del_responsable == "ForeignKeyViolation":
        raise HTTPException(status_code=409, detail="No se puede eliminar el Responsable, es referenciado por otros registros")
    else:
        raise HTTPException(status_code=404, detail="Responsable not found")

@methods.delete("/rol-deleted/{rol_id}", response_model=schemas.Roles, tags=['Routes Delete'])
def delete_rol(rol_id: int, db: Session = Depends(get_db)):
    del_rol = crud.delete_rol(db = db, rol_id = rol_id)
    if del_rol == "Deleted Rol":
        return JSONResponse(content={"detail": "Rol deleted OK"}, status_code=200)
    elif del_rol == "ForeignKeyViolation":
        raise HTTPException(status_code=409, detail="No se puede eliminar el Rol, es referenciado por otros registros")
    else:
        raise HTTPException(status_code=404, detail="rol not found")

@methods.delete("/sede-deleted/{sede_id}", response_model=schemas.Sede, tags=['Routes Delete'])
def delete_sede(sede_id: int, db: Session = Depends(get_db)):
    del_sede = crud.delete_sede(db = db, sede_id = sede_id)
    if del_sede == "Deleted Rol":
        return JSONResponse(content={"detail": "Rol deleted OK"}, status_code=200)
    elif del_sede == "ForeignKeyViolation":
        raise HTTPException(status_code=409, detail="No se puede eliminar la Sede, es referenciada por otros registros")
    else:
        raise HTTPException(status_code=404, detail="rol not found")

@methods.delete("/proveedor-deleted/{proveedor_id}", response_model=schemas.Proveedor, tags=['Routes Delete'])
def delete_proveedor(proveedor_id: int, db: Session = Depends(get_db)):
    del_proveedor = crud.delete_proveedor(db = db, proveedor_id = proveedor_id)
    if del_proveedor == "Deleted Proveedor":
        return JSONResponse(content={"detail": "Proveedor deleted OK"}, status_code=200)
    elif del_proveedor == "ForeignKeyViolation":
        raise HTTPException(status_code=409, detail="No se puede eliminar el proveedor, es referenciado por otros registros")
    else:
        raise HTTPException(status_code=404, detail="rol not found")

@methods.delete("/producto-deleted/{producto_id}", response_model=schemas.Producto, tags=['Routes Delete'])
def delete_producto(producto_id: int, db: Session = Depends(get_db)):
    del_producto = crud.delete_producto(db = db, producto_id = producto_id)
    if del_producto == "Deleted Producto":
        return JSONResponse(content={"detail": "Proveedor deleted OK"}, status_code=200)
    else:
        raise HTTPException(status_code=409, detail="No se puede eliminar el producto, es referenciado por otros registros")

@methods.delete("/ubicacion-deleted/{ubicacion_id}", response_model=schemas.Producto, tags=['Routes Delete'])
def delete_ubicacion(ubicacion_id: int, db: Session = Depends(get_db)):
    del_ubicacion = crud.delete_ubicacion(db = db, ubicacion_id = ubicacion_id)
    if del_ubicacion == "Deleted Ubicacion":
        return JSONResponse(content={"detail": "Ubicacion deleted OK"}, status_code=200)
    else:
        raise HTTPException(status_code=409, detail="No se puede eliminar la ubicacion, es referenciada por otros registros")

@methods.delete("/mantenimiento-deleted/{mantenimiento_id}", response_model=schemas.Mantenimiento, tags=['Routes Delete'])
def del_mantenimiento(mantenimiento_id: int, db: Session = Depends(get_db)):
    del_mante = crud.delete_mantenimiento(db = db, mantenimiento_id = mantenimiento_id)
    if del_mante == "Deleted Mantenimiento":
        return JSONResponse(content={"detail": "Mantenimiento deleted OK"}, status_code=200)
    elif del_mante == "ForeignKeyViolation":
        raise HTTPException(status_code=409, detail="No se puede eliminar el Mantenimiento, es referenciado por otros registros")
    else:
        raise HTTPException(status_code=404, detail="mantenimiento not found")

@methods.delete("/categoria-deleted/{categoria_id}", response_model=schemas.Categoria, tags=['Routes Delete'])
def del_categoria(categoria_id: int, db: Session = Depends(get_db)):
    del_cate = crud.delete_categoria(db = db, categoria_id = categoria_id)
    if del_cate == "Deleted Categoria":
        return JSONResponse(content={"detail": "Categoria deleted OK"}, status_code=200)
    elif del_cate == "ForeignKeyViolation":
        raise HTTPException(status_code=409, detail="No se puede eliminar la Categoria, es referenciada por otros registros")
    else:
        raise HTTPException(status_code=404, detail="categoria not found")

@methods.delete("/proveedor-mantenimiento-deleted/{proveedor_mante_id}", response_model=schemas.ProveedorMantenimiento, tags=['Routes Delete'])
def del_prove_mante(proveedor_mante_id: int, db: Session = Depends(get_db)):
    del_pro_m = crud.delete_proveedor_mante(db = db, proveedor_mante_id = proveedor_mante_id)
    if del_pro_m == "Deleted Mantenimiento del proveedor":
        return JSONResponse(content={"detail": "Mantenimiento del proveedor deleted OK"}, status_code=200)
    elif del_pro_m == "ForeignKeyViolation":
        raise HTTPException(status_code=409, detail="No se puede eliminar el mantenimiento del proveedor, es referenciada por otros registros")
    else:
        raise HTTPException(status_code=404, detail="Mantenimiento del proveedor not found")

@methods.delete("/usuario-deleted/{usuario_id}", response_model=schemas.Usuarios, tags=['Routes Delete'])
def del_mantenimiento(usuario_id: int, db: Session = Depends(get_db)):
    del_user = crud.delete_usuario(db = db, usuario_id = usuario_id)
    if del_user == "Deleted Usuario":
        return JSONResponse(content={"detail": "Usuario deleted OK"}, status_code=200)
    elif del_user == "ForeignKeyViolation":
        raise HTTPException(status_code=409, detail="No se puede eliminar el Usuario, es referenciado por otros registros")
    else:
        raise HTTPException(status_code=404, detail="user not found")


