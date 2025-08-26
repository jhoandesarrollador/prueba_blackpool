from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
import math

from app.db.database import get_db
from app.core.dependencies import get_current_user
from app.crud.cliente import cliente_crud
from app.schemas.cliente import Cliente, ClienteCreate, ClienteUpdate, ClienteList
from app.schemas.user import User
from app.models.cliente import TipoClienteEnum

router = APIRouter(prefix="/clientes", tags=["clientes"])

@router.post("/", response_model=Cliente, status_code=status.HTTP_201_CREATED)
async def crear_cliente(
    cliente_data: ClienteCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Crear un nuevo cliente"""
    try:
        # Verificar si ya existe cliente con mismo email o número de cuenta
        existing_email = await cliente_crud.get_by_email(db, cliente_data.correo_electronico)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un cliente con este correo electrónico"
            )
        
        existing_account = await cliente_crud.get_by_numero_cuenta(db, cliente_data.numero_cuenta)
        if existing_account:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un cliente con este número de cuenta"
            )
        
        cliente = await cliente_crud.create(db, cliente_data)
        return cliente
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.get("/{cliente_id}", response_model=Cliente)
async def obtener_cliente(
    cliente_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Consultar un cliente por su ID"""
    cliente = await cliente_crud.get_by_id(db, cliente_id)
    
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado"
        )
    
    return cliente

@router.put("/{cliente_id}", response_model=Cliente)
async def actualizar_cliente(
    cliente_id: int,
    cliente_update: ClienteUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Actualizar los datos de un cliente existente"""
    try:
        # Verificar si el cliente existe
        existing_cliente = await cliente_crud.get_by_id(db, cliente_id)
        if not existing_cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente no encontrado"
            )
        
        # Si se está actualizando email o número de cuenta, verificar unicidad
        if cliente_update.correo_electronico:
            existing_email = await cliente_crud.get_by_email(db, cliente_update.correo_electronico)
            if existing_email and existing_email.id != cliente_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ya existe un cliente con este correo electrónico"
                )
        
        if cliente_update.numero_cuenta:
            existing_account = await cliente_crud.get_by_numero_cuenta(db, cliente_update.numero_cuenta)
            if existing_account and existing_account.id != cliente_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ya existe un cliente con este número de cuenta"
                )
        
        cliente = await cliente_crud.update(db, cliente_id, cliente_update)
        return cliente
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.get("/", response_model=ClienteList)
async def listar_clientes(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    page: int = Query(1, ge=1, description="Número de página"),
    size: int = Query(10, ge=1, le=100, description="Tamaño de página"),
    nombre: Optional[str] = Query(None, description="Filtrar por nombre"),
    tipo_cliente: Optional[TipoClienteEnum] = Query(None, description="Filtrar por tipo de cliente")
):
    """Consultar todos los clientes con paginación y filtros"""
    try:
        skip = (page - 1) * size
        
        clientes, total = await cliente_crud.get_all(
            db=db,
            skip=skip,
            limit=size,
            nombre=nombre,
            tipo_cliente=tipo_cliente.value if tipo_cliente else None
        )
        
        total_pages = math.ceil(total / size) if total > 0 else 1
        
        return ClienteList(
            clientes=clientes,
            total=total,
            page=page,
            size=size,
            pages=total_pages
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_cliente(
    cliente_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Eliminar un cliente"""
    try:
        cliente_eliminado = await cliente_crud.delete(db, cliente_id)
        
        if not cliente_eliminado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente no encontrado"
            )
        
        return None
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

# Endpoints adicionales útiles

@router.get("/buscar/email/{email}", response_model=Cliente)
async def buscar_por_email(
    email: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Buscar cliente por email"""
    cliente = await cliente_crud.get_by_email(db, email)
    
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado"
        )
    
    return cliente

@router.get("/buscar/cuenta/{numero_cuenta}", response_model=Cliente)
async def buscar_por_numero_cuenta(
    numero_cuenta: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Buscar cliente por número de cuenta"""
    cliente = await cliente_crud.get_by_numero_cuenta(db, numero_cuenta)
    
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado"
        )
    
    return cliente