from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, APIRouter, status, Response, Request, Form
from . import models, schemas 
from typing import List
from sqlalchemy.exc import IntegrityError
from .security import get_password_hash
from datetime import datetime, date
from sqlalchemy.exc import IntegrityError
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse


# obtener un responsable
def get_responsable(db: Session, responsable_id: int):
    return db.query(models.Responsable).filter(models.Responsable.id == responsable_id).first()

# obtener todos los responsables
def get_all_responsables(db: Session) -> List[models.Responsable]:
    return db.query(models.Responsable).all()

# crear un responsable
def create_responsable(db: Session, responsable: schemas.ResponsableCreate):
    db_responsable = models.Responsable(**responsable.dict())
    db.add(db_responsable)
    db.commit()
    db.refresh(db_responsable)
    return db_responsable

# Actualizar un responsable
def update_responsable(db: Session, responsable_id: int, nombre: str, correo: str, telefono: str):
    responsable = db.query(models.Responsable).filter(models.Responsable.id == responsable_id).first()
    if responsable:
        responsable.nombre = nombre
        responsable.correo = correo
        responsable.telefono = telefono
        db.commit()
        db.refresh(responsable)  # Asegúrate de devolver el objeto actualizado
        return responsable
    return None


# eliminar un responsable

def delete_responsable(db: Session, responsable_id: int):
    try:
        result = db.query(models.Responsable).filter(models.Responsable.id == responsable_id).delete(synchronize_session=False)
        db.commit()
        if result == 0:
            return "Not Found"
        return "Deleted Responsable"
    except IntegrityError:
        db.rollback()
        return "ForeignKeyViolation"

# logs users
def get_user_by_username(db: Session, nombre: str):
    return db.query(models.Usuarios).filter(models.Usuarios.nombre == nombre).first()

def create_user(db: Session, usuario: schemas.UsuariosCreate):
    hashed_password = get_password_hash(usuario.password)  
    db_user = models.Usuarios(
        nombre=usuario.nombre,
        correo=usuario.correo,
        hashed_password=hashed_password,
        estado=usuario.estado,
        fecha_creacion=usuario.fecha_creacion,
        id_rol=usuario.id_rol
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    # redirigir a la seccion de usuarios
    from app.main import app
    return RedirectResponse(url=app.url_path_for("usuarios_main"), status_code=status.HTTP_303_SEE_OTHER) 
