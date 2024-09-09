from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Text, Float
from sqlalchemy.orm import relationship
from .database import Base

# Modelo Categoria
class Categoria(Base):
    __tablename__ = "categoria"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, index=True)
    
    productos = relationship("Producto", back_populates="categoria")
# Modelo Sede
class Sede(Base):
    __tablename__ = "sede"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, index=True)
    direccion = Column(String(200), nullable=False)
    telefono = Column(String(20))
    
    productos = relationship("Producto", back_populates="sede")

# Modelo Responsable
class Responsable(Base):
    __tablename__ = "responsable"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, index=True)
    correo = Column(String(200), nullable=False, index=True)
    telefono = Column(String(20))
    
    productos = relationship("Producto", back_populates="responsable")
# Modelo Roles
class Roles(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(250), nullable=False, index=True)
    
    usuarios = relationship("Usuarios", back_populates="rol")

# Modelo Usuarios
class Usuarios(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nombre = Column(String(250),unique=True , nullable=False, index=True)
    correo = Column(String(250), unique=True , nullable=False, index=True)
    hashed_password = Column(String(100), nullable=False)
    estado = Column(String(25))
    fecha_creacion = Column(Date, nullable=False)   
    id_rol = Column(Integer, ForeignKey("roles.id"))

    rol = relationship("Roles", back_populates="usuarios")
    mantenimiento = relationship("Mantenimiento", back_populates="usuarios")

# Modelo Proveedor
class Proveedor(Base):
    __tablename__ = "proveedor"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False, index=True)
    direccion = Column(String(200))
    telefono = Column(String(20))
    
    productos = relationship("Producto", back_populates="proveedor")

# Modelo Producto
class Producto(Base):
    __tablename__ = "producto"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    id_responsable = Column(Integer, ForeignKey("responsable.id"))
    codigo = Column(String(200), nullable=False, index=True)
    id_sede = Column(Integer, ForeignKey("sede.id"))
    cantidad = Column(Integer)
    uso = Column(Text)
    estado = Column(String(100))
    fecha_mantenimiento = Column(Date)
    costo_inicial = Column(Float)
    modo = Column(String(200))
    observacion = Column(Text)
    id_categoria = Column(Integer, ForeignKey("categoria.id"))
    id_proveedor = Column(Integer, ForeignKey("proveedor.id"))
    fecha_ingreso = Column(Date, nullable=False)

    responsable = relationship("Responsable", back_populates="productos")
    sede = relationship("Sede", back_populates="productos")
    categoria = relationship("Categoria", back_populates="productos")
    proveedor = relationship("Proveedor", back_populates="productos")
    mantenimiento = relationship("Mantenimiento", back_populates="producto")

# Modelo Ubicacion
class Ubicacion(Base):
    __tablename__ = "ubicacion"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nombre = Column(String(200), nullable=False)
    id_sede = Column(Integer, ForeignKey("sede.id"))

    sede = relationship("Sede")

# Modelo Producto_Proveedores
class ProductoProveedores(Base):
    __tablename__ = "producto_proveedores"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_producto = Column(Integer, ForeignKey("producto.id"))
    id_proveedor = Column(Integer, ForeignKey("proveedor.id"))

    producto = relationship("Producto")
    proveedor = relationship("Proveedor")

# Modelo Producto_Mantenimiento
class Proveedormantenimiento(Base):
    __tablename__ = "proveedormantenimiento"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)
    direccion = Column(String(200))
    telefono = Column(String(20))
    contacto = Column(String(200))
    id_producto = Column(Integer, ForeignKey("producto.id"))

    producto = relationship("Producto")

# Modelo Mantenimiento
class Mantenimiento(Base):
    __tablename__ = "mantenimiento"
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha_mantenimiento = Column(Date)
    observacion = Column(Text)
    id_usuarios = Column(Integer, ForeignKey("usuarios.id"))
    id_producto = Column(Integer, ForeignKey("producto.id"))

    usuarios = relationship("Usuarios", back_populates="mantenimiento")
    producto = relationship("Producto", back_populates="mantenimiento")

