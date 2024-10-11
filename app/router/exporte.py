import pandas as pd
from fastapi import FastAPI, Depends, File, UploadFile, HTTPException, APIRouter, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from .. import crud, models
from ..database import SessionLocal, engine
from ..security import get_password_hash
from ..crud import get_cod_producto, get_user_by_username
from fastapi.responses import StreamingResponse
import io

models.Base.metadata.create_all(bind=engine)
exporte = APIRouter()

def get_bd():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@exporte.get("/exporte-modelos/{model_name}", tags=['Routes Pandas'])
def exportar(model_name: str, tipo_archivo: str = 'csv', db: Session = Depends(get_bd)):
    try: 
        MODELS = {
            'Sede': models.Sede,
            'Categoria': models.Categoria,
            'Responsable': models.Responsable,
            'Roles': models.Roles,
            'Usuarios': models.Usuarios,
            'Proveedor': models.Proveedor,
            'Producto': models.Producto,
            'Ubicacion': models.Ubicacion,
            'Mantenimiento': models.Mantenimiento,
            'ProductoProveedores': models.ProductoProveedores,
            'ProveedorMantenimiento': models.Proveedormantenimiento
        }

        if model_name not in MODELS:
            raise HTTPException(status_code=404, detail=f"Modelo {model_name} no encontrado")

        modelClass = MODELS[model_name]
        records = db.query(modelClass).order_by(modelClass.id).all()

        if not records:
            raise HTTPException(status_code=400, detail='No hay registros de este modelo en la base de datos')
        
        # Función para manejar atributos de registros
        def safe_getattr(record, column):
            value = getattr(record, column.name)
            if isinstance(value, (list, dict)):
                return str(value)
            return value

        # Crear diccionario de registros
        records_dic = [{column.name: safe_getattr(record, column) for column in modelClass.__table__.columns} for record in records]
        
        buffer = io.BytesIO()          
        if tipo_archivo == 'xlsx':
            # Guardar como archivo Excel
            df_records = pd.DataFrame(records_dic)
            df_records.to_excel(buffer, index=False, engine='openpyxl')
            buffer.seek(0)
            response = StreamingResponse(buffer, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response.headers["Content-Disposition"] = f"attachment; filename={model_name}.xlsx"
        else:
            # Guardar como archivo CSV
            df_records = pd.DataFrame(records_dic)
            try:
                df_records.to_csv(buffer, index=False, encoding='utf-8')  # Especifica la codificación
            except Exception as e:
                raise HTTPException(status_code=500, detail=f'Error al escribir CSV: {e}')
                
            buffer.seek(0)
            response = StreamingResponse(buffer, media_type="text/csv")
            response.headers["Content-Disposition"] = f"attachment; filename={model_name}.csv"

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error {e}')
