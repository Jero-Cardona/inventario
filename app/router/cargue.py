import pandas as pd
from fastapi import FastAPI, Depends, File, Form, UploadFile, HTTPException, APIRouter, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from .. import crud, models
from ..database import SessionLocal, engine
from ..security import get_password_hash
from ..crud import get_cod_producto, get_user_by_username
import logging
from sqlalchemy import String, cast

# Inicializar logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

models.Base.metadata.create_all(bind=engine)
cargue = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

MODEL_CONFIG = {
    'Sede': {
        'model': models.Sede,
        'columns': {
            'nombre': 'nombre',
            'direccion': 'dirección',
            'telefono': 'telefono'
        }
    },
    'Categoria': {
        'model': models.Categoria,
        'columns': {
            'nombre' : 'nombre',
        }
    },
    'Responsable': {
        'model': models.Responsable,
        'columns': {
            'nombre': 'nombre',
            'correo': 'correo',
            'telefono': 'telefono',
        }
    },
    'Roles': {
        'model': models.Roles,
        'columns': {
            'nombre': 'nombre',
        }
    },
    'Usuarios':{
        'model': models.Usuarios,
        'columns': {
            'nombre': 'nombre',
            'correo': 'correo',
            'hashed_password': 'contraseña',
            'estado': 'estado',
            'fecha_creacion': 'fecha_creacion',
            'id_rol': 'rol',
        }
    },
    'Proveedor':{
        'model': models.Proveedor,
        'columns': {
            'nombre': 'nombre',
            'direccion': 'dirección',
            'telefono': 'telefono',
        }
    },
    'Producto':{
        'model': models.Producto,
        'columns': {
            'id_responsable': 'responsable',
            'codigo': 'codigo',
            'id_sede': 'sede',
            'cantidad': 'cantidad',
            'uso': 'uso',
            'estado': 'estado',
            'fecha_mantenimiento': 'fecha_mantenimiento',
            'costo_inicial': 'costo_inicial',
            'modo': 'modo',
            'observacion': 'observaciones',
            'id_categoria': 'categoria',
            'id_proveedor': 'proveedor',
            'fecha_ingreso': 'fecha_ingreso',
        }
    },
    'Ubicacion':{
        'model': models.Ubicacion,
        'columns': {
            'nombre': 'nombre',
            'id_sede': 'sede',
        }
    },
    'Mantenimiento':{
        'model': models.Mantenimiento,
        'columns': {
            'fecha_mantenimiento': 'fecha_mantenimiento',
            'observacion': 'observacion',
            'id_usuarios': 'usuario',
            'id_producto': 'cod_producto',
        }
    },
    'ProductoProveedores':{
        'model':models.ProductoProveedores,
        'columns': {
            'id_producto': 'producto',
            'id_proveedor': 'proveedor',
        }
    },
}



@cargue.post("/cargue-archivos", tags=['Routes Pandas'])
def cargar(file: UploadFile = File(...), nombre_modelo: str = Form(...), db: Session = Depends(get_db)):

    if file.content_type not in ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.ms-excel"]:
        raise HTTPException(status_code=400, detail="El archivo debe ser un Excel")

    if nombre_modelo not in MODEL_CONFIG:
        raise HTTPException(status_code=400, detail=f"Modelo {nombre_modelo} no configurado")

    model_config = MODEL_CONFIG[nombre_modelo]
    expected_columns = model_config['columns'].values()

    try:
        df_archivos = pd.read_excel(file.file, usecols=expected_columns)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Error al leer el archivo: {e}')
    
    if not all(column in df_archivos.columns for column in expected_columns):
        raise HTTPException(status_code=400, detail=f"El archivo debe contener las siguientes columnas: {', '.join(expected_columns)}")
    
    # mapeo de id a traves del nombre
    def get_foreign_key_id(model, value, db, nombre_modelo, field='nombre'):

        if pd.isna(value) or value is None:
            return None

        if nombre_modelo == 'Producto' and hasattr(model, 'codigo'):
            field = 'codigo'
            value = str(value)
        else:
            field = 'nombre'
        entity = db.query(model).filter(getattr(model, field) == value).first()
        if not entity:
            raise HTTPException(status_code=400, detail=f"{model.__name__} con {field} '{value}' no encontrado")
        return entity.id

    try:
        model = model_config['model']
        column_mapping = model_config['columns']

        for index, row in df_archivos.iterrows():
            record_data = {}
            
            for attr, col in column_mapping.items():
                if attr == 'id_responsable':
                    record_data[attr] = get_foreign_key_id(models.Responsable, row[col], db, 'Responsable')
                elif attr == 'id_sede':
                    record_data[attr] = get_foreign_key_id(models.Sede, row[col], db, 'Sede')
                elif attr == 'id_categoria':
                    record_data[attr] = get_foreign_key_id(models.Categoria, row[col], db, 'Categoria')
                elif attr == 'id_proveedor':
                    record_data[attr] = get_foreign_key_id(models.Proveedor, row[col], db, 'Proveedor')
                elif attr == 'id_usuarios':
                    record_data[attr] = get_foreign_key_id(models.Usuarios, row[col], db, 'Usuarios')
                elif attr == 'id_producto':
                    record_data[attr] = get_foreign_key_id(models.Producto, row[col], db, 'Producto')
                elif attr == 'id_rol':
                    record_data[attr] = get_foreign_key_id(models.Roles, row[col], db, 'Roles')
                elif attr == 'hashed_password':
                    record_data[attr] = get_password_hash(row[col])
                elif attr == 'codigo':
                    if get_cod_producto(db, str(row[col])):
                        raise HTTPException(status_code=400, detail=f"El código '{row[col]}' ya existe en la base de datos.")
                    record_data[attr] = str(row[col])
                else:
                    record_data[attr] = row[col]
            
            # Crear la instancia del modelo (Producto, Usuario, etc.)
            new_record = model(**record_data)
            db.add(new_record)
            db.commit()  # Primero, insertar el producto
            db.refresh(new_record)  # Refrescar para obtener el id generado

            if isinstance(new_record, models.Producto) and record_data.get('id_proveedor') is not None:
                producto_proveedor = models.ProductoProveedores(
                    id_producto=new_record.id,
                    id_proveedor=record_data['id_proveedor']
                )
                db.add(producto_proveedor)
            
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Error al insertar en la base de datos: {e}')
    return {"message": "Archivo cargado y registros creados correctamente"}
