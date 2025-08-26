from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import enum

Base = declarative_base()

class TipoClienteEnum(str, enum.Enum):
    INDIVIDUAL = "individual"
    CORPORATIVO = "corporativo"
    VIP = "vip"

class EstadoCivilEnum(str, enum.Enum):
    SOLTERO = "soltero"
    CASADO = "casado"
    DIVORCIADO = "divorciado"
    VIUDO = "viudo"

class GeneroEnum(str, enum.Enum):
    MASCULINO = "masculino"
    FEMENINO = "femenino"
    OTRO = "otro"

class Cliente(Base):
    __tablename__ = "clientes"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    numero_cuenta = Column(String(20), unique=True, index=True, nullable=False)
    saldo = Column(Float, default=0.0)
    fecha_nacimiento = Column(Date, nullable=False)
    direccion = Column(String(255))
    telefono = Column(String(20))
    correo_electronico = Column(String(100), unique=True, index=True)
    tipo_cliente = Column(Enum(TipoClienteEnum), default=TipoClienteEnum.INDIVIDUAL)
    estado_civil = Column(Enum(EstadoCivilEnum))
    numero_identificacion = Column(String(20), unique=True, index=True)
    profesion = Column(String(100))
    genero = Column(Enum(GeneroEnum))
    nacionalidad = Column(String(50))
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())