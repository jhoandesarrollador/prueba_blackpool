from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from sqlalchemy.exc import IntegrityError
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)

from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteUpdate

class ClienteCRUD:
    
    async def create(self, db: AsyncSession, cliente_data: ClienteCreate) -> Cliente:
        """Crear un nuevo cliente"""
        try:
            logger.info("Iniciando creación en CRUD")
            
            # Crear instancia del modelo
            cliente_dict = cliente_data.model_dump()
            logger.info(f"Datos del cliente: {cliente_dict}")
            
            cliente = Cliente(**cliente_dict)
            logger.info("Instancia de Cliente creada")
            
            db.add(cliente)
            logger.info("Cliente agregado a sesión")
            
            await db.commit()
            logger.info("Commit exitoso")
            
            await db.refresh(cliente)
            logger.info(f"Cliente refrescado, ID: {cliente.id}")
            
            return cliente
            
        except IntegrityError as e:
            logger.error(f"IntegrityError: {str(e)}")
            await db.rollback()
            raise ValueError("Cliente con datos únicos ya existe (email, cuenta o identificación)")
        except Exception as e:
            logger.error(f"Error inesperado en create: {str(e)}", exc_info=True)
            await db.rollback()
            raise
    
    async def get_by_id(self, db: AsyncSession, cliente_id: int) -> Optional[Cliente]:
        """Obtener cliente por ID"""
        result = await db.execute(select(Cliente).where(Cliente.id == cliente_id))
        return result.scalar_one_or_none()
    
    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[Cliente]:
        """Obtener cliente por email"""
        result = await db.execute(select(Cliente).where(Cliente.correo_electronico == email))
        return result.scalar_one_or_none()
    
    async def get_by_numero_cuenta(self, db: AsyncSession, numero_cuenta: str) -> Optional[Cliente]:
        """Obtener cliente por número de cuenta"""
        result = await db.execute(select(Cliente).where(Cliente.numero_cuenta == numero_cuenta))
        return result.scalar_one_or_none()
    
    async def get_all(
        self, 
        db: AsyncSession, 
        skip: int = 0, 
        limit: int = 100,
        nombre: Optional[str] = None,
        tipo_cliente: Optional[str] = None
    ) -> tuple[List[Cliente], int]:
        """Obtener todos los clientes con paginación y filtros"""
        query = select(Cliente)
        
        # Aplicar filtros
        filters = []
        if nombre:
            filters.append(Cliente.nombre.ilike(f"%{nombre}%"))
        if tipo_cliente:
            filters.append(Cliente.tipo_cliente == tipo_cliente)
        
        if filters:
            query = query.where(and_(*filters))
        
        # Contar total primero - CORREGIDO
        count_query = select(func.count(Cliente.id))
        if filters:
            count_query = count_query.where(and_(*filters))
        
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        # Obtener resultados con paginación
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        clientes = result.scalars().all()
        
        return list(clientes), total
    
    async def update(
        self, 
        db: AsyncSession, 
        cliente_id: int, 
        cliente_update: ClienteUpdate
    ) -> Optional[Cliente]:
        """Actualizar cliente"""
        cliente = await self.get_by_id(db, cliente_id)
        if not cliente:
            return None
        
        update_data = cliente_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(cliente, field, value)
        
        try:
            await db.commit()
            await db.refresh(cliente)
            return cliente
        except IntegrityError:
            await db.rollback()
            raise ValueError("Datos únicos ya existen (email, cuenta o identificación)")
    
    async def delete(self, db: AsyncSession, cliente_id: int) -> bool:
        """Eliminar cliente"""
        cliente = await self.get_by_id(db, cliente_id)
        if not cliente:
            return False
        
        await db.delete(cliente)
        await db.commit()
        return True

# Instancia global del CRUD
cliente_crud = ClienteCRUD()