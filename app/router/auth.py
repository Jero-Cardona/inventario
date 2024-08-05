from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from .. import schemas, models, crud, security
from ..database import SessionLocal, engine
from ..security import create_access_token, SECRET_KEY, ALGORITHM
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from typing import Optional
from app.schemas import *
from jose import jwt, JWTError
import logging
from starlette.requests import Request




models.Base.metadata.create_all(bind=engine)
# prodeccion de rutas
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")
router = APIRouter()
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="No se logro validar las credenciales",
    headers={"WWW-Authenticate": "Bearer"},
)
def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        token_decode = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        nombre_usuario: str = token_decode.get("sub")
        logging.info(f"Payload: {token_decode}")
        if nombre_usuario is None:
            raise credentials_exception
    except JWTError as e:
        logging.error(f"JWT Error: {e}")
        raise credentials_exception
    usuario = crud.get_user_by_username(db, nombre=nombre_usuario)
    if not usuario:
        logging.error(f"JWT Error: {e}")
        raise credentials_exception
    return usuario

# continuar con el error
def get_user_disabled_current(usuario: Usuarios = Depends(get_current_user)):
    if usuario.estado == 'inactivo':
        raise HTTPException(status_code=400, detail='Usuario Inactivo')
    return usuario


@router.post("/crear-usuario/", response_model=schemas.Usuarios, tags=['Users'])
def register_user(usuario: schemas.UsuariosCreate = Depends(schemas.UsuariosCreate.as_form), db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, nombre=usuario.nombre)
    if db_user:
        raise HTTPException(status_code=400, detail="Este nombre de usuario ya fue registrado")
    return crud.create_user(db=db, usuario=usuario)

@router.post("/login/", tags=['Users'])
def login_for_access_token(request: Request, db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    usuario = crud.get_user_by_username(db, nombre=form_data.username)
    if not usuario or not security.verify_password(form_data.password, usuario.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nombre de Usuario o Contraseña incorrecta",
            headers={"WWW-Authenticate": "Bearer"},
        )
    request.session['nombre'] = usuario.nombre
    access_token = security.create_access_token(data={"sub": usuario.nombre})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/", response_class=HTMLResponse, tags=['Users'])
def login_form(request: Request):
    return templates.TemplateResponse("login2.html", {"request": request})

@router.get("/login2", response_class=HTMLResponse, tags=['Users'])
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

