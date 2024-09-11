from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.responses import JSONResponse, RedirectResponse
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from starlette.middleware.base import BaseHTTPMiddleware
from . import models 
import logging
from .security import SECRET_KEY, ALGORITHM

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

logger = logging.getLogger(__name__)
login = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

# Creacion del middleware para los usuarios Activos
class VerifyUserActive(BaseHTTPMiddleware):
    excluded_routes = ["/login/", "/", "/bloquear-usuario", "/activar-usuario", "/static", "/docs", "/openapi.json"]

    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/static"):
            return await call_next(request)

        if request.url.path in self.excluded_routes:
            return await call_next(request)

        db: Session = next(get_db())  
        token = request.cookies.get("access_token")
        if token is None:
            request.cookies.clear()
            return login
        try:
            payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username is None:
                raise HTTPException(status_code=403, detail="Invalid token.")
            user = db.query(models.Usuarios).filter(models.Usuarios.nombre == username).first()
            if user is None:
                return JSONResponse(status_code=403, content={"detail": "User not found"})
            # add request propieryties
            request.state.id_rol = user.id_rol
            if user.estado != "activo":
                return JSONResponse(status_code=403, content={"detail": "Este Usuario se encuentra inactivo "})
        except JWTError:
            return JSONResponse(status_code=403, content={"detail": "Invalid token."})

        response = await call_next(request)
        return response

# Creacion del middleware para las acciones del Admin
class AdminUser(BaseHTTPMiddleware):
    excluded_routes = ["/login/", "/", "/salir", "/bloquear-usuario", "/activar-usuario",
                    "/static", "/docs", "/openapi.json", "/inicio", "/favicon.ico",
                    "/proveedor-section", "/categoria-section", "/rol-section",
                    "/reportes-section", "/sede-section", "/responsable-section",
                    "/producto-section", "/usuario-section", "/mantenimiento-section",]

    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/static"):
            return await call_next(request)

        if request.url.path in self.excluded_routes:
            return await call_next(request)
        
        db: Session = next(get_db())  
        token = request.cookies.get("access_token")
        if token is None:
            request.cookies.clear()
            return login
        try:
            payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username is None:
                raise HTTPException(status_code=403, detail="Invalid token.")
            usuario = db.query(models.Usuarios).filter(models.Usuarios.nombre == username).first()
            if usuario is None:
                return JSONResponse(status_code=403, content={"detail": "User not found"})
            request.state.id_rol = usuario.id_rol
            request.state.estado = usuario.estado
            if usuario.id_rol != 1 :
                return JSONResponse(status_code=403, content={"detail": "Solo Administradores pueden realizar esta funcion"})
        except JWTError:
            return JSONResponse(status_code=403, content={"detail": "Invalid token."})
        
        response = await call_next(request)
        return response
