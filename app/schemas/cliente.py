from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import date, datetime
from app.models.cliente import TipoClienteEnum, EstadoCivilEnum, GeneroEnum

# Base schema con campos comunes
class ClienteBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    apellido: str = Field(..., min_length=2, max_length=100)
    numero_cuenta: str = Field(..., min_length=10, max_length=20)
    saldo: float = Field(default=0.0, ge=0)
    fecha_nacimiento: date
    direccion: Optional[str] = Field(None, max_length=255)
    telefono: Optional[str] = Field(None, max_length=20)
    correo_electronico: EmailStr
    tipo_cliente: TipoClienteEnum = TipoClienteEnum.INDIVIDUAL
    estado_civil: Optional[EstadoCivilEnum] = None
    numero_identificacion: str = Field(..., min_length=5, max_length=20)
    profesion: Optional[str] = Field(None, max_length=100)
    genero: Optional[GeneroEnum] = None
    nacionalidad: Optional[str] = Field(None, max_length=50)

    @validator('fecha_nacimiento')
    def validate_fecha_nacimiento(cls, v):
        today = date.today()
        age = today.year - v.year - ((today.month, today.day) < (v.month, v.day))
        if age < 18:
            raise ValueError('El cliente debe ser mayor de 18 años')
        if age > 120:
            raise ValueError('Fecha de nacimiento no válida')
        return v

# Schema para crear cliente
class ClienteCreate(ClienteBase):
    pass

# Schema para actualizar cliente (todos los campos opcionales)
class ClienteUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    apellido: Optional[str] = Field(None, min_length=2, max_length=100)
    numero_cuenta: Optional[str] = Field(None, min_length=10, max_length=20)
    saldo: Optional[float] = Field(None, ge=0)
    fecha_nacimiento: Optional[date] = None
    direccion: Optional[str] = Field(None, max_length=255)
    telefono: Optional[str] = Field(None, max_length=20)
    correo_electronico: Optional[EmailStr] = None
    tipo_cliente: Optional[TipoClienteEnum] = None
    estado_civil: Optional[EstadoCivilEnum] = None
    numero_identificacion: Optional[str] = Field(None, min_length=5, max_length=20)
    profesion: Optional[str] = Field(None, max_length=100)
    genero: Optional[GeneroEnum] = None
    nacionalidad: Optional[str] = Field(None, max_length=50)

    @validator('fecha_nacimiento')
    def validate_fecha_nacimiento(cls, v):
        if v is None:
            return v
        today = date.today()
        age = today.year - v.year - ((today.month, today.day) < (v.month, v.day))
        if age < 18:
            raise ValueError('El cliente debe ser mayor de 18 años')
        if age > 120:
            raise ValueError('Fecha de nacimiento no válida')
        return v

# Schema para respuesta (incluye campos de DB como id, created_at, etc.)
class Cliente(ClienteBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Schema para listado con paginación
class ClienteList(BaseModel):
    clientes: list[Cliente]
    total: int
    page: int
    size: int
    pages: int