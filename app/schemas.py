from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional
from datetime import date
from app.schemas import *
from fastapi import Form

# Modelo Categoria
class CategoriaBase(BaseModel):
    nombre: str

class CategoriaCreate(CategoriaBase):
    pass

class Categoria(CategoriaBase):
    id: int

    class Config:
        from_attributes = True
        
# Modelo Sede
class SedeBase(BaseModel):
    nombre: str
    direccion: str
    telefono: Optional[str] = None

class SedeCreate(SedeBase):
    pass

class Sede(SedeBase):
    id: int
    
    class Config:
        from_attributes = True

# Modelo Responsable
class ResponsableBase(BaseModel):
    nombre: str
    correo: str
    telefono: Optional[str] = None
    
    def __dict__(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "telefono": self.telefono
        }

class ResponsableCreate(ResponsableBase):
    pass

class Responsable(ResponsableBase):
    id: int
    
    class Config:
        from_attributes = True

# Modelo Roles
class RolesBase(BaseModel):
    nombre: str

class RolesCreate(RolesBase):
    pass

class Roles(RolesBase):
    id: int
    
    class Config:
        from_attributes = True

# Modelo Usuarios
class UsuariosBase(BaseModel):
    nombre: str = Field(..., alias="nombre")
    correo: Optional[str] = Field(None, alias="correo")
    hashed_password: str = Field(..., alias="hashed_password")
    estado: Optional[str] = Field(None, alias="estado")
    fecha_creacion: Optional[date] = Field(..., alias="fecha_creacion")
    id_rol: int = Field(..., alias="id_rol")

    @classmethod
    def as_form(
        cls,
        nombre: str = Form(...),
        correo: Optional[str] = Form(None),
        hashed_password: str = Form(...),
        estado: Optional[str] = Form(None),
        id_rol: int = Form(...),
        fecha_creacion: Optional[date] = Form(...),
    ):
        return cls(
            nombre=nombre,
            correo=correo,
            hashed_password=hashed_password,
            estado=estado,
            id_rol=id_rol,
            fecha_creacion=fecha_creacion,
        )

class UsuariosCreate(UsuariosBase):
    pass

class Usuarios(UsuariosBase):
    id: int
    rol: Roles  

    def dict(self, *args, **kwargs):
        data = super().dict(*args, **kwargs)
        data['rol'] = self.rol.nombre if self.rol else None 
        return data

    class Config:
        from_attributes = True
        
# Modelo Proveedor
class ProveedorBase(BaseModel):
    nombre: str
    direccion: Optional[str] = None
    telefono: Optional[str] = None

class ProveedorCreate(BaseModel):
    pass

class Proveedor(ProveedorBase):
    id: int
    
    class Config:
        from_attributes = True

# Model para producto
class ProductoBase(BaseModel):
    id_responsable: int = Field(..., alias="id_responsable")
    codigo: str = Field(..., alias="codigo")
    id_sede: int = Field(..., alias="id_sede")
    cantidad: Optional[int] = Field(None, alias="cantidad")
    uso: Optional[str] = Field(None, alias="uso")
    estado: Optional[str] = Field(None, alias="estado")
    fecha_mantenimiento: Optional[date] = Field(None, alias="fecha_mantenimiento")
    costo_inicial: Optional[float] = Field(None, alias="costo_inicial")
    modo: Optional[str] = Field(None, alias="modo")
    observacion: Optional[str] = Field(None, alias="observacion")
    id_categoria: int = Field(..., alias="id_categoria")
    id_proveedor: int = Field(..., alias="id_proveedor")
    fecha_ingreso: Optional[date] = Field(..., alias="fecha_ingreso")
    

    @classmethod
    def as_form(
        cls,
        id_responsable: int = Form(...),
        codigo: str = Form(...),
        id_sede: int = Form(...),
        cantidad: Optional[int] = Form(None),
        uso: Optional[str] = Form(None),
        estado: Optional[str] = Form(None),
        fecha_mantenimiento: Optional[date] = Form(None),
        costo_inicial: Optional[float] = Form(None),
        modo: Optional[str] = Form(None),
        observacion: Optional[str] = Form(None),
        id_categoria: int = Form(...),
        id_proveedor: int = Form(...),
        fecha_ingreso: Optional[date] = Form(...)
    ):
        return cls(
            id_responsable=id_responsable,
            codigo=codigo,
            id_sede=id_sede,
            cantidad=cantidad,
            uso=uso,
            estado=estado,
            fecha_mantenimiento=fecha_mantenimiento,
            costo_inicial=costo_inicial,
            modo=modo,
            observacion=observacion,
            id_categoria=id_categoria,
            id_proveedor=id_proveedor,
            fecha_ingreso=fecha_ingreso
        )

class ProductoCreate(ProductoBase):
    pass

class Producto(ProductoBase):
    id: int
    responsable: Responsable
    sede: Sede
    categoria: Categoria
    proveedor: Proveedor
    
    class Config:
        from_attributes = True

# Modelo Ubicacion
class UbicacionBase(BaseModel):
    nombre: str
    id_sede: int

class UbicacionCreate(UbicacionBase):
    pass

class Ubicacion(UbicacionBase):
    id: int
    sede: Sede
    
    class Config:
        from_attributes = True

# Modelo Producto_proveedores
class Producto_ProvBase(BaseModel):
    id_producto: int
    id_proveedor: int

class ProductoProveedoresCreate(Producto_ProvBase):
    pass

class ProductoProveedores(Producto_ProvBase):
    id: int
    producto: Producto
    proveedor: Proveedor
    
    class Config:
        from_attributes = True

# Modelo Proveedor_Mantenimiento
class Proveedor_MBase(BaseModel):
    nombre: str
    direccion: Optional[str] = None
    contacto: Optional[str] = None
    telefono: Optional[str] = None
    id_producto: int

class Proveedor_MCreate(Proveedor_MBase):
    pass

class Proveedor_M(Proveedor_MBase):
    id: int
    producto: Producto
    
    class Config:
        from_attributes = True

# Modelo Mantenimento
class MantenimientoBase(BaseModel):
    fecha_mantenimiento: Optional[date] = None
    observacion: Optional[str] = None
    id_usuarios: int
    id_producto: int

class MantenimientoCreate(MantenimientoBase):
    pass

class Mantenimiento(MantenimientoBase):
    id: int
    usuarios: Usuarios
    producto: Producto
    
    class Config:
        from_attributes = True
