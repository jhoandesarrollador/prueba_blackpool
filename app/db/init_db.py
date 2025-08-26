from sqlalchemy.ext.asyncio import create_async_engine
from app.models.cliente import Base
from app.models.user import User
from app.core.config import settings
from app.core.auth import get_password_hash
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

async def init_database():
    """Inicializar base de datos y crear usuario admin por defecto"""
    
    # Crear engine
    engine = create_async_engine(settings.DATABASE_URL, echo=True)
    
    # Crear todas las tablas
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Crear usuario admin por defecto
    AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with AsyncSessionLocal() as session:
        # Verificar si ya existe admin
        from sqlalchemy import select
        result = await session.execute(select(User).where(User.username == "admin"))
        admin_user = result.scalar_one_or_none()
        
        if not admin_user:
            admin_user = User(
                username="admin",
                email="admin@fintechbank.com",
                hashed_password=get_password_hash("admin123"),
                is_admin=True
            )
            session.add(admin_user)
            await session.commit()
            print("Usuario admin creado: admin / admin123")
        else:
            print("Usuario admin ya existe")
    
    await engine.dispose()

if __name__ == "__main__":
    import asyncio
    asyncio.run(init_database())