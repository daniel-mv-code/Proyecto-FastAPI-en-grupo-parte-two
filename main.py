from fastapi import FastAPI, HTTPException, Path, Query, status
from typing import Optional, List
# Importamos los modelos formales desde nuestro nuevo archivo
from models import ClienteModel, VehiculoModel, RepuestoModel, MecanicoModel

app = FastAPI(title="Sistema de Diagnóstico Automotriz PRO")

# --- BASE DE DATOS EN MEMORIA ---
clientes = [
    {"id": 1, "nombre": "Brayan", "ciudad": "Bogotá"},
    {"id": 2, "nombre": "Hermenegildo", "ciudad": "Medellín"}
]

vehiculos = [
    {"id": 1, "placa": "ABC123", "modelo": "Mazda 3", "cliente_id": 1, "color": "Rojo"},
    {"id": 2, "placa": "XYZ789", "modelo": "Chevrolet Spark", "cliente_id": 2, "color": "Gris"}
]

mecanicos = [
    {"id": 1, "nombre": "Eustaquio", "especialidad": "Motor"},
    {"id": 2, "nombre": "Albeiro", "especialidad": "Frenos"}
]

repuestos = [
    {"id": 1, "nombre": "Embrague", "precio": 80000.0, "categoria": "Transmisión"},
    {"id": 2, "nombre": "Cuello de la Transmision", "precio": 25000.0, "categoria": "Transmisión"},
    {"id": 3, "nombre": "Pastillas", "precio": 45000.0, "categoria": "Frenos"}
]

# --- RUTAS DE CLIENTES ---

@app.get("/clientes", tags=["Clientes"])
def obtener_clientes(
    nombre: Optional[str] = Query(None, min_length=3),
    ciudad: Optional[str] = Query(None)
):
    resultado = clientes
    if nombre:
        resultado = [c for c in resultado if nombre.lower() in c["nombre"].lower()]
    if ciudad:
        resultado = [c for c in resultado if c["ciudad"].lower() == ciudad.lower()]
    return {"clientes": resultado}

@app.get("/clientes/{cliente_id}/vehiculos/{vehiculo_id}", tags=["Clientes"])
def obtener_vehiculo_cliente(
    cliente_id: int = Path(..., gt=0),
    vehiculo_id: int = Path(..., gt=0)
):
    v = next((v for v in vehiculos if v["id"] == vehiculo_id and v["cliente_id"] == cliente_id), None)
    if not v:
        raise HTTPException(status_code=404, detail="Relación Cliente-Vehículo no encontrada")
    return v

# --- RUTAS DE VEHÍCULOS ---

@app.get("/vehiculos/buscar", tags=["Vehículos"])
def buscar_vehiculos(
    modelo: Optional[str] = Query(None),
    color: Optional[str] = Query(None)
):
    res = [v for v in vehiculos if (not modelo or modelo in v["modelo"]) and (not color or color == v["color"])]
    return {"resultados": res}

@app.get("/vehiculos/verificar/{id}/{placa}", tags=["Vehículos"])
def verificar_vehiculo(
    id: int = Path(..., gt=0),
    placa: str = Path(..., min_length=6, max_length=6)
):
    v = next((v for v in vehiculos if v["id"] == id and v["placa"] == placa), None)
    if not v:
        raise HTTPException(status_code=404, detail="Vehículo no coincide con los registros")
    return v

# --- RUTAS DE REPUESTOS ---

@app.get("/repuestos/filtrar", tags=["Repuestos"])
def filtrar_repuestos(
    precio_max: Optional[int] = Query(None, gt=0),
    categoria: Optional[str] = Query(None)
):
    res = repuestos
    if precio_max:
        res = [r for r in res if r["precio"] <= precio_max]
    if category := categoria:
        res = [r for r in res if r["categoria"].lower() == category.lower()]
    return res

@app.get("/repuestos/detalle/{id}/{slug_nombre}", tags=["Repuestos"])
def detalle_repuesto(
    id: int = Path(..., gt=0),
    slug_nombre: str = Path(...)
):
    r = next((r for r in repuestos if r["id"] == id), None)
    if not r:
        raise HTTPException(status_code=404, detail="Repuesto no encontrado")
    return {"repuesto": r, "seo_check": slug_nombre}

# --- RUTAS DE ESCRITURA MODIFICADAS CON VALIDACIÓN PYDANTIC ---

@app.post("/clientes", status_code=status.HTTP_201_CREATED, tags=["Clientes"])
def crear_cliente(cliente: ClienteModel):
    # Validamos duplicados
    if any(c["id"] == cliente.id for c in clientes):
        raise HTTPException(status_code=400, detail="El ID del cliente ya existe")
    
    nuevo_cliente = cliente.model_dump()
    clientes.append(nuevo_cliente)
    return {"mensaje": "Cliente agregado exitosamente", "cliente": nuevo_cliente}

@app.put("/vehiculos/{id}", tags=["Vehículos"])
def actualizar_vehiculo(id: int, datos: VehiculoModel):
    for v in vehiculos:
        if v["id"] == id:
            v.update(datos.model_dump())
            return {"mensaje": "Vehículo actualizado con éxito", "vehiculo": v}
    raise HTTPException(status_code=404, detail="Vehículo no encontrado")

@app.delete("/repuestos/{id}", tags=["Repuestos"])
def eliminar_repuesto(id: int):
    for r in repuestos:
        if r["id"] == id:
            repuestos.remove(r)
            return {"mensaje": "Repuesto eliminado correctamente"}
    raise HTTPException(status_code=404, detail="Repuesto no encontrado")

@app.get("/", tags=["Inicio"])
def inicio():
    return {"mensaje": "API Sistema de Diagnóstico Automotriz activa"}  # Paréntesis corregido aquí