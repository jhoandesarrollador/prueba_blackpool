# FinTechBank API

API para la gestión de clientes bancarios, desarrollada con FastAPI y SQLAlchemy en modo asíncrono.

## Características

*   **Framework Asíncrono:** Construido con FastAPI para alta eficiencia.
*   **Base de Datos:** Utiliza SQLAlchemy para interactuar con una base de datos MySQL de forma asíncrona.
*   **Autenticación:** Sistema de autenticación basado en JWT (JSON Web Tokens).
*   **Validación de Datos:** Uso de Pydantic para una validación de datos robusta y clara.
*   **Operaciones CRUD:** Endpoints completos para la gestión de clientes y usuarios.
*   **Dockerización:** Listo para desplegar con Docker.

## Tecnologías

*   **Python 3.11**
*   **FastAPI**
*   **SQLAlchemy 2.0**
*   **Pydantic**
*   **Uvicorn**
*   **MySQL (con `aiomysql`)**
*   **Docker**

## Instalación

### Prerrequisitos

*   Python 3.11 o superior
*   Docker (opcional, para ejecución en contenedor)
*   Una instancia de MySQL en ejecución

### Configuración del Entorno Virtual

1.  **Clonar el repositorio:**
    ```bash
    git clone <URL-DEL-REPOSITORIO>
    cd prueba_blackpool
    ```

2.  **Crear y activar un entorno virtual:**
    ```bash
    python -m venv venv
    # En Windows
    venv\Scripts\activate
    # En macOS/Linux
    source venv/bin/activate
    ```

3.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

### Configuración de la Aplicación

1.  **Crear un archivo `.env`** en la raíz del proyecto.

2.  **Configurar las variables de entorno en `.env`:**
    ```env
    DATABASE_URL="mysql+aiomysql://<user>:<password>@<host>:<port>/<database>"
    SECRET_KEY="<tu-clave-secreta-muy-segura>"
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```
    **Importante:** La `SECRET_KEY` debe ser una cadena de texto larga y aleatoria.

### Ejecución Local

Para iniciar la aplicación localmente, ejecuta el siguiente comando desde la raíz del proyecto:

```bash
uvicorn app.main:app --reload
```

La API estará disponible en `http://127.0.0.1:8000`.

## Uso con Docker

1.  **Construir la imagen de Docker:**
    ```bash
    docker build -t fintech-api .
    ```

2.  **Ejecutar el contenedor:**
    Asegúrate de pasar las variables de entorno necesarias.
    ```bash
    docker run -d -p 8000:8000 \
      -e DATABASE_URL="mysql+aiomysql://<user>:<password>@<host>:<port>/<database>" \
      -e SECRET_KEY="<tu-clave-secreta-muy-segura>" \
      --name fintech-api-container \
      fintech-api
    ```

## Estructura del Proyecto

```
├── app/
│   ├── api/          # Routers y endpoints de la API
│   ├── core/         # Lógica de negocio y configuración
│   ├── crud/         # Operaciones de acceso a datos (CRUD)
│   ├── db/           # Configuración de la base de datos
│   ├── models/       # Modelos de SQLAlchemy
│   └── schemas/      # Esquemas de Pydantic
├── .dockerignore
├── .gitignore
├── Dockerfile
├── README.md
└── requirements.txt
```

## Endpoints de la API

Una vez que la aplicación esté en ejecución, puedes acceder a la documentación interactiva de la API en:

*   **Swagger UI:** `http://127.0.0.1:8000/docs`
*   **ReDoc:** `http://127.0.0.1:8000/redoc`

### Autenticación

*   `POST /api/v1/auth/register`: Registrar un nuevo usuario.
*   `POST /api/v1/auth/login`: Iniciar sesión y obtener un token de acceso.

### Clientes

*   `POST /api/v1/clientes/`: Crear un nuevo cliente.
*   `GET /api/v1/clientes/`: Listar todos los clientes con paginación.
*   `GET /api/v1/clientes/{cliente_id}`: Obtener un cliente por su ID.
*   `PUT /api/v1/clientes/{cliente_id}`: Actualizar un cliente.
*   `DELETE /api/v1/clientes/{cliente_id}`: Eliminar un cliente.
*   `GET /api/v1/clientes/buscar/email/{email}`: Buscar un cliente por su email.
*   `GET /api/v1/clientes/buscar/cuenta/{numero_cuenta}`: Buscar un cliente por su número de cuenta.

