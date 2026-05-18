from pydantic import BaseModel, Field
from typing import List

# --- 1. MODELO CLIENTE ---
class ClienteModel(BaseModel):
    id: int = Field(..., gt=0, description="El ID debe ser un número entero positivo")
    nombre: str = Field(..., min_length=2, max_length=50, description="El nombre debe tener al menos 2 letras")
    ciudad: str = Field(..., min_length=3, description="La ciudad no puede estar vacía")

# --- 2. MODELO VEHÍCULO ---
class VehiculoModel(BaseModel):
    id: int = Field(..., gt=0, description="ID del vehículo mayor a 0")
    placa: str = Field(..., min_length=6, max_length=6, description="La placa debe tener exactamente 6 caracteres")
    modelo: str = Field(..., min_length=2, description="El modelo/marca no puede estar vacío")
    cliente_id: int = Field(..., gt=0, description="ID del propietario válido")
    color: str = Field(..., min_length=3, description="El color debe especificarse")

# --- 3. MODELO MECÁNICO ---
class MecanicoModel(BaseModel):
    id: int = Field(..., gt=0, description="ID del mecánico mayor a 0")
    nombre: str = Field(..., min_length=3, description="Nombre del operario")
    especialidad: str = Field(..., min_length=3, description="Área de especialización técnica")

# --- 4. MODELO REPUESTO ---
class RepuestoModel(BaseModel):
    id: int = Field(..., gt=0, description="ID del repuesto")
    nombre: str = Field(..., min_length=3, description="Nombre de la autoparte o repuesto")
    precio: float = Field(..., gt=0, description="El precio comercial debe ser mayor a 0")
    categoria: str = Field(..., min_length=3, description="Categoría del sistema del vehículo")