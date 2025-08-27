import asyncio
import typer
import sys
import re
from pathlib import Path
from sqlalchemy import select
from email_validator import validate_email, EmailNotValidError

# Añadir el directorio raíz del proyecto al sys.path
sys.path.insert(0, Path(__file__).resolve().parents[1].as_posix())

from app.db.database import AsyncSessionLocal, engine
from app.models.user import User
from app.core.auth import get_password_hash

app = typer.Typer()

def is_password_strong_enough(password: str) -> bool:
    """Verifica que la contraseña cumpla con los requisitos de seguridad."""
    if len(password) < 8:
        print(f"\033[91mError: La contraseña debe tener al menos 8 caracteres.\033[0m")
        return False
    if not re.search(r"[A-Z]", password):
        print(f"\033[91mError: La contraseña debe contener al menos una letra mayúscula.\033[0m")
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        print(f"\033[91mError: La contraseña debe contener al menos un carácter especial.\033[0m")
        return False
    return True

async def create_admin_user(username: str, email: str, password: str):
    """Lógica para crear el usuario admin en la base de datos."""
    async with AsyncSessionLocal() as session:
        # Verificar si el usuario o el email ya existen
        result = await session.execute(select(User).where(
            (User.username == username) | (User.email == email)
        ))
        if result.scalar_one_or_none():
            print(f"\033[91mError: El usuario '{username}' o el email '{email}' ya existen.\033[0m")
            return

        # Crear el nuevo usuario administrador
        hashed_password = get_password_hash(password)
        admin_user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            is_active=True,
            is_admin=True
        )
        
        session.add(admin_user)
        await session.commit()
        print(f"\033[92m¡Usuario administrador '{username}' creado exitosamente!\033[0m")
    
    # Cerrar el pool de conexiones del engine
    await engine.dispose()

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    Crea un usuario administrador inicial de forma interactiva y segura.
    """
    print("--- Creación de Usuario Administrador ---")
    
    # Solicitar datos de forma interactiva
    username = typer.prompt("Nombre de usuario para el administrador")
    
    while True:
        email_input = typer.prompt("Email para el administrador")
        try:
            # Validar el formato del email
            validate_email(email_input)
            break  # Si es válido, salimos del bucle
        except EmailNotValidError as e:
            # Si no es válido, mostramos un error y volvemos a pedirlo
            print(f"\033[91mError: El email no es válido: {e}. Inténtalo de nuevo.\033[0m")

    while True:
        password = typer.prompt("Contraseña para el administrador (no se mostrará)", hide_input=True)
        if is_password_strong_enough(password):
            password_confirm = typer.prompt("Confirma la contraseña", hide_input=True)
            if password == password_confirm:
                break
            else:
                print("\033[91mError: Las contraseñas no coinciden.\033[0m")
        else:
            print("\033[93mPor favor, elige una contraseña más segura.\033[0m")


    # Ejecutar la lógica asíncrona
    asyncio.run(create_admin_user(username, email_input, password))

if __name__ == "__main__":
    app()
