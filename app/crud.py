from sqlalchemy.orm import Session, joinedload
from fastapi import FastAPI, Depends, HTTPException, APIRouter, status, Response, Request, Form
from . import models, schemas 
from typing import List, Optional
from sqlalchemy.exc import IntegrityError
from .security import get_password_hash
from datetime import datetime, date
from sqlalchemy.exc import IntegrityError
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse

# obtener el codigo del producto unico
def get_cod_producto(db: Session, codigo: str):
    return db.query(models.Producto).filter(models.Producto.codigo == codigo).first()

# obtener registro por id
def get_responsable(responsable_id: int, db: Session):
    responsable = db.query(models.Responsable).filter(models.Responsable.id == responsable_id).first()
    if not responsable:
        raise HTTPException(status_code=404, detail='Responsable not found')
    return responsable

def get_usuario(usuarios_id: int, db: Session):
    usuario = db.query(models.Usuarios).filter(models.Usuarios.id == usuarios_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail='User  not found')
    return usuario

def get_producto(producto_id: int, db: Session):
    producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail='Product not found')
    return producto

def get_producto_for_qr(producto_id: int, db: Session):
    producto = db.query(models.Producto).filter(models.Producto.id == producto_id).options(
        joinedload(models.Producto.responsable), joinedload(models.Producto.sede),
        joinedload(models.Producto.categoria), joinedload(models.Producto.proveedor)).first()
    if not producto:
        raise HTTPException(status_code=404, detail='Product not found')
    return producto

def get_all_productos_for_qr(db: Session) -> List[models.Producto]:
    productos = db.query(models.Producto).options(
        joinedload(models.Producto.responsable), joinedload(models.Producto.sede),
        joinedload(models.Producto.categoria), joinedload(models.Producto.proveedor)).order_by(
            models.Producto.id
        ).all()
    if not productos:
        raise HTTPException(status_code=404, detail='Error Products not founds')
    return productos

def get_proveedor(proveedor_id: int, db: Session):
    proveedor = db.query(models.Proveedor).filter(models.Proveedor.id == proveedor_id).first()
    if not proveedor:
        raise HTTPException(status_code=404, detail='Proveedor not found')
    return proveedor

def get_sede(sede_id: int, db: Session):
    sede = db.query(models.Sede).filter(models.Sede.id == sede_id).first()
    if not sede:
        raise HTTPException(status_code=404, detail='Sede not found')
    return sede

def get_categoria(categoria_id: int, db: Session):
    categoria = db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail='Categoria not found')
    return categoria

def get_mantenimiento(mantenimiento_id: int, db: Session):
    mantenimiento = db.query(models.Mantenimiento).filter(models.Mantenimiento.id == mantenimiento_id).first()
    if not mantenimiento:
        raise HTTPException(status_code=404, detail='Mantenimiento not found')
    return mantenimiento

def get_rol(rol_id: int, db: Session):
    rol = db.query(models.Roles).filter(models.Roles.id == rol_id).first()
    if not rol:
        raise HTTPException(status_code=404, detail='Rol not found')
    return rol

def get_ubicacion(ubicacion_id: int, db: Session):
    ubicacion = db.query(models.Ubicacion).filter(models.Ubicacion.id == ubicacion_id).first()
    if not ubicacion:
        raise HTTPException(status_code=404, detail='Ubicacacion not found')
    return ubicacion

def get_producto_proveedor(id_consult: int, db: Session):
    producto_proveedor = db.query(models.ProductoProveedores).filter(models.ProductoProveedores.id == id_consult).first()
    if not producto_proveedor:
        raise HTTPException(status_code=404, detail='Product and Proveedor not found')
    return producto_proveedor

def get_proveedor_mantenimiento(id_consult: int, db: Session):
    proveedor_mantenimiento = db.query(models.Proveedormantenimiento).filter(models.Proveedormantenimiento.id == id_consult).first()
    if not proveedor_mantenimiento:
        raise HTTPException(status_code=404, detail='Product and Proveedor not found')
    return proveedor_mantenimiento

# obtener todos los registros
def get_all_responsables(db: Session) -> List[models.Responsable]:
    return db.query(models.Responsable).order_by(models.Responsable.id.asc()).all()

def get_all_productos(db: Session) -> List[models.Producto]:
    return db.query(models.Producto).order_by(models.Producto.id.asc()).all()

def get_all_usuarios(db: Session) -> List[models.Usuarios]:
    return db.query(models.Usuarios).order_by(models.Usuarios.id.asc()).all()

def get_all_categorias(db: Session) -> List[models.Categoria]:
    return db.query(models.Categoria).order_by(models.Categoria.id.asc()).all()

def get_all_sedes(db: Session) -> List[models.Sede]:
    return db.query(models.Sede).order_by(models.Sede.id.asc()).all()

def get_all_proveedores(db: Session) -> List[models.Proveedor]:
    return db.query(models.Proveedor).order_by(models.Proveedor.id.asc()).all()

def get_all_roles(db: Session) -> List[models.Roles]:
    return db.query(models.Roles).order_by(models.Roles.id.asc()).all()

def get_all_mantenimientos(db: Session) -> List[models.Mantenimiento]:
    return db.query(models.Mantenimiento).order_by(models.Mantenimiento.id.asc()).all()

def get_all_ubicaciones(db: Session) -> list[models.Ubicacion]:
    return db.query(models.Ubicacion).order_by(models.Ubicacion.id.asc()).all()

# Funciones de Actualizar Datos
def update_responsable(db: Session, responsable_id: int, nombre: str, correo: str, telefono: str):
    try:
        responsable = db.query(models.Responsable).filter(models.Responsable.id == responsable_id).first()
        if responsable:
            responsable.nombre = nombre
            responsable.correo = correo
            responsable.telefono = telefono
            db.commit()
            db.refresh(responsable) 
            return responsable
        return None
    except Exception as e:
        db.rollback()  
        raise e  

def update_m(db: Session, mantenimiento_id: int, fecha_mantenimiento: date, observacion: str, id_usuarios: int, id_producto: int):
    try:
        mantenimiento = db.query(models.Mantenimiento).filter(models.Mantenimiento.id == mantenimiento_id).first()
        if mantenimiento:
            mantenimiento.fecha_mantenimiento = fecha_mantenimiento
            mantenimiento.observacion = observacion
            mantenimiento.id_usuarios = id_usuarios
            mantenimiento.id_producto = id_producto
            db.commit()
            db.refresh(mantenimiento) 
            return mantenimiento
        return None
    except Exception as e:
        db.rollback()  
        raise e  

def update_ubication(db: Session, ubicacion_id: int, nombre: str, id_sede: int, id_producto: int):
    try:
        ubicacion = db.query(models.Ubicacion).filter(models.Ubicacion.id == ubicacion_id).first()
        if ubicacion:
            ubicacion.nombre = nombre
            ubicacion.id_sede = id_sede
            ubicacion.id_producto = id_producto
            db.commit()
            db.refresh(ubicacion)
            return ubicacion
        return None
    except Exception as e:
        db.rollback()
        raise e

def update_user(db: Session, usuario_id: int, nombre: str, correo: str, hashed_password: str,
                estado: str, fecha_creacion: date, id_rol: int):
    db_user = db.query(models.Usuarios).filter(models.Usuarios.id == usuario_id).first()
    if db_user:
        db_user.nombre = nombre
        db_user.correo = correo
        if db_user.hashed_password:
            db_user.hashed_password = get_password_hash(hashed_password)     
        db_user.estado = estado
        db_user.fecha_creacion = fecha_creacion
        db_user.id_rol = id_rol
        db.commit()
        db.refresh(db_user)
        return db_user
    return None

def update_proveedor(db: Session, proveedor_id: int, nombre: str, direccion: str, telefono: str):
    proveedor = db.query(models.Proveedor).filter(models.Proveedor.id == proveedor_id).first()
    if proveedor:
        proveedor.nombre = nombre
        proveedor.direccion = direccion
        proveedor.telefono = telefono
        db.commit()
        db.refresh(proveedor)
        return proveedor
    return None

def update_producto(db: Session, producto_id: int, id_responsable: int, codigo: str, id_sede: int, cantidad: int, uso: str, 
                    estado: str, fecha_mantenimiento: date, costo_inicial: float, modo: str, observacion: str,
                    id_categoria: int, fecha_ingreso: date, id_proveedor: Optional[int] = None):
    db_producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()

    if db_producto:
        db_producto.id_responsable = id_responsable
        db_producto.codigo = codigo
        db_producto.id_sede = id_sede
        db_producto.cantidad = cantidad
        db_producto.uso = uso
        db_producto.estado = estado
        db_producto.fecha_mantenimiento = fecha_mantenimiento
        db_producto.costo_inicial = costo_inicial
        db_producto.modo = modo
        db_producto.observacion = observacion
        db_producto.id_categoria = id_categoria
        db_producto.fecha_ingreso = fecha_ingreso

        if id_proveedor is not None:
            db_producto.id_proveedor = id_proveedor

            db_proveedor = db.query(models.ProductoProveedores).filter(
                models.ProductoProveedores.id_producto == producto_id).first()

            if db_proveedor:
                db_proveedor.id_proveedor = id_proveedor
                db.commit()
                db.refresh(db_proveedor)
            else:
                new_producto_proveedor = models.ProductoProveedores(
                    id_producto=producto_id,
                    id_proveedor=id_proveedor
                )
                db.add(new_producto_proveedor)
                db.commit()
                db.refresh(new_producto_proveedor)

        elif db_producto.id_proveedor is not None:
            db_proveedor = db.query(models.ProductoProveedores).filter(
                models.ProductoProveedores.id_producto == producto_id).first()

            if db_proveedor:
                db.delete(db_proveedor)
                db.commit()

            db_producto.id_proveedor = None

        db.commit()
        db.refresh(db_producto)

        return db_producto

    return None


def update_sede(db: Session, sede_id: int, nombre: str, direccion: str, telefono: str):
    sede = db.query(models.Sede).filter(models.Sede.id == sede_id).first()
    if sede:
        sede.nombre = nombre
        sede.direccion = direccion
        sede.telefono = telefono
        db.commit()
        db.refresh(sede)
        return sede
    return None

def update_categoria(db: Session, categoria_id: int, nombre: str, depreciacion: float):
    try:
        categoria = db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()
        if categoria:
            categoria.nombre = nombre
            categoria.depreciacion = depreciacion
            db.commit()
            db.refresh(categoria)
            return categoria
        return None
    except Exception as e:
        db.rollback()
        raise e

def update_proveedor_m(db: Session, proveedor_mante_id: int, contacto: str, id_proveedor:int, id_producto: int):
    try:
        proveedor_mante = db.query(models.Proveedormantenimiento).filter(models.Proveedormantenimiento.id == proveedor_mante_id).first()
        if proveedor_mante:
            proveedor_mante.contacto = contacto
            proveedor_mante.id_proveedor = id_proveedor
            proveedor_mante.id_producto = id_producto
            db.commit()
            db.refresh(proveedor_mante)
            return proveedor_mante
        return None
    except Exception as e:
        db.rollback()
        raise e

def update_rol(db: Session, rol_id: int, nombre: str):
    try:
        rol = db.query(models.Roles).filter(models.Roles.id == rol_id).first()
        if rol:
            rol.nombre = nombre
            db.commit()
            db.refresh(rol)
            return rol
        return None
    except Exception as e:
        db.rollback()
        raise e

# Funciones de Eliminar datos
def delete_responsable(db: Session, responsable_id: int):
    try:
        result = db.query(models.Responsable).filter(models.Responsable.id == responsable_id).delete(synchronize_session=False)
        if result == 0:
            return "Not Found"
        db.commit()
        return "Deleted Responsable"
    except IntegrityError:
        db.rollback()
        return "ForeignKeyViolation"

def delete_rol(db: Session, rol_id: int):
    try:
        result = db.query(models.Roles).filter(models.Roles.id == rol_id).delete(synchronize_session=False)
        if result == 0:
            return "Not found"
        db.commit()
        return "Deleted Rol"
    except IntegrityError:
        db.rollback()
        return "ForeignKeyViolation"
        
def delete_producto(db: Session, producto_id: int):
    try:
        result = db.query(models.Producto).filter(models.Producto.id == producto_id).delete(synchronize_session=False)
        if result == 0:
            return "Not found"
        db.commit()
        return "Deleted Producto"
    except IntegrityError as e:
        db.rollback()
        return e

def delete_categoria(db: Session, categoria_id: int):
    try:
        result = db.query(models.Categoria).filter(models.Categoria.id == categoria_id).delete(synchronize_session=False)
        if result == 0:
            return "Not found"
        db.commit()
        return "Deleted Categoria"
    except IntegrityError:
        db.rollback()
        return "ForeignKeyViolation"

def delete_sede(db: Session, sede_id: int):
    try:
        result = db.query(models.Sede).filter(models.Sede.id == sede_id).delete(synchronize_session=False)
        if result == 0:
            return "Not found"
        db.commit()
        return "Deleted Sede"
    except IntegrityError:
        db.rollback()
        return "ForeignKeyViolation"

def delete_mantenimiento(db: Session, mantenimiento_id: int):
    try:
        result = db.query(models.Mantenimiento).filter(models.Mantenimiento.id == mantenimiento_id).delete(synchronize_session=False)
        if result == 0:
            return "Not found"
        db.commit()
        return "Deleted Mantenimiento"
    except IntegrityError:
        db.rollback()
        return "ForeignKeyViolation"

def delete_proveedor(db: Session, proveedor_id: int):
    try:
        result = db.query(models.Proveedor).filter(models.Proveedor.id == proveedor_id).delete(synchronize_session=False)
        if result == 0:
            return "Not found"
        db.commit()
        return "Deleted Proveedor"
    except IntegrityError:
        db.rollback()
        return "ForeignKeyViolation"

def delete_ubicacion(db: Session, ubicacion_id: int):
    try:
        result = db.query(models.Ubicacion).filter(models.Ubicacion.id == ubicacion_id).delete(synchronize_session=False)
        if result == 0:
            return "Not found"
        db.commit()
        return "Deleted Ubicacion"
    except IntegrityError:
        db.rollback()
        return "ForeignKeyViolation"

def delete_usuario(db: Session, usuario_id: int):
    try:
        result = db.query(models.Usuarios).filter(models.Usuarios.id == usuario_id).delete(synchronize_session=False)
        if result == 0:
            return "Not found"
        db.commit()
        return "Deleted Usuario"
    except IntegrityError:
        db.rollback()
        return "ForeignKeyViolation"

def delete_proveedor_mante(db: Session, proveedor_mante_id: int):
    try:
        result = db.query(models.Proveedormantenimiento).filter(models.Proveedormantenimiento.id == proveedor_mante_id).delete(synchronize_session=False)
        if result == 0:
            return "Not found"
        db.commit()
        return "Deleted Mantenimiento del proveedor"
    except IntegrityError:
        db.rollback()
        return "ForeignKeyViolation"

# logs users
def get_user_by_username(db: Session, nombre: str):
    return db.query(models.Usuarios).filter(models.Usuarios.nombre == nombre).first()

def get_user_by_id(db: Session, usuario_id: int):
    return db.query(models.Usuarios).filter(models.Usuarios.id == usuario_id).first()

def create_user(db: Session, usuario: schemas.UsuariosCreate):
    hashed_password = get_password_hash(usuario.hashed_password)  
    db_user = models.Usuarios(
        nombre=usuario.nombre,
        correo=usuario.correo,
        hashed_password=hashed_password,
        estado=usuario.estado,
        fecha_creacion=usuario.fecha_creacion,
        id_rol=usuario.id_rol,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return RedirectResponse(url="/usuario-section", status_code=status.HTTP_303_SEE_OTHER)

# calcular la depreciacion de un producto
def calcular_valor_actual(producto):
    # Datos importantes
    fecha_ingreso = producto.fecha_ingreso
    costo_inicial = producto.costo_inicial
    porcentaje_m = producto.categoria.depreciacion  # Depreciación mensual en porcentaje 
    
    fecha_actual = datetime.now().date()
    days_pass = (fecha_actual - fecha_ingreso).days
    years_pass = (fecha_actual - fecha_ingreso).days / 365.25  # Considera años bisiestos
    
    depreciacion_acumulada = ((porcentaje_m * 12) / 100) * costo_inicial * years_pass
    valor_actual = costo_inicial - depreciacion_acumulada
    
    if valor_actual < 0:
        valor_actual = 0
        
    valor = round(valor_actual, 1)
    return valor

# funcion para el calculo de cada categoria
def depreciacion_categorias(db: Session):
    productos = db.query(models.Producto).all()
    categorias = db.query(models.Categoria).all()
    
    depreciacion_por_categoria = {categoria.id:0 for categoria in categorias}
    suma_costos_categoria = {categoria.id:0 for categoria in categorias}
    
    resultado = []
    for producto in productos:
        valor_actual = calcular_valor_actual(producto)
        
        if producto.id_categoria:
            depreciacion_por_categoria[producto.id_categoria] += valor_actual
        
        resultado = []
        for categoria in categorias:
            total_valor_actual = f"{depreciacion_por_categoria[categoria.id]:,.2f}"
            resultado.append({
                "categoria": categoria.nombre,
                "total_valor_actual": total_valor_actual
            })
    # costos actuales
    return resultado

