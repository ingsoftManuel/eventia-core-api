# Eventia Core API

Una API REST moderna construida con **FastAPI** para la gestión de eventos, integrando bases de datos PostgreSQL, caché Redis y análisis de seguridad.

## 🚀 Características

- **FastAPI**: Framework web de alto rendimiento
- **PostgreSQL**: Base de datos relacional robusta
- **Redis**: Caché en memoria para optimización
- **Pydantic**: Validación de datos con tipado fuerte
- **SQLAlchemy**: ORM para manejo de base de datos
- **Bandit**: Análisis de seguridad automatizado
- **Pytest**: Suite completa de testing (unit, integration, system)
- **CI/CD**: Pipeline automático con GitHub Actions

## 📋 Requisitos Previos

- Python 3.12+
- PostgreSQL 15+
- Redis 7+
- pip (gestor de paquetes Python)

## 🔧 Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone <tu-repo-url>
   cd eventia-core-api
   ```

2. **Crear entorno virtual:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # En Windows
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno:**
   ```bash
   copy .env.example .env
   # Editar .env con tus credenciales
   ```

## 🗄️ Base de Datos

### Inicializar migraciones:
```bash
alembic upgrade head
```

### Crear nueva migración:
```bash
alembic revision --autogenerate -m "Descripción del cambio"
```

## ▶️ Ejecutar la Aplicación

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

La API estará disponible en: `http://localhost:8000`

**Documentación interactiva:** `http://localhost:8000/docs`

## 🧪 Testing

### Ejecutar todos los tests:
```bash
pytest tests/ -v
```

### Tests por tipo:
```bash
pytest tests/unit/ -v          # Tests unitarios
pytest tests/integration/ -v   # Tests de integración
pytest tests/system/ -v        # Tests del sistema
```

### Cobertura de código:
```bash
pytest --cov=src tests/
```

## 🔒 Análisis de Seguridad

```bash
bandit -r src/
```

## 📁 Estructura del Proyecto

```
eventia-core-api/
├── src/
│   ├── main.py              # Entrada de la aplicación
│   ├── api/                 # Rutas y endpoints
│   ├── models/              # Modelos de base de datos
│   ├── schemas/             # Esquemas Pydantic
│   ├── services/            # Lógica de negocio
│   └── config.py            # Configuración
├── tests/
│   ├── unit/                # Tests unitarios
│   ├── integration/         # Tests de integración
│   └── system/              # Tests del sistema
├── migrations/              # Migraciones de Alembic
├── requirements.txt         # Dependencias Python
└── .github/workflows/       # CI/CD Pipeline
```

## 🔌 Variables de Entorno

```env
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/eventia_db
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
SECRET_KEY=tu-clave-secreta
DEBUG=False
```

## 📦 Dependencias Principales

| Librería | Versión | Uso |
|----------|---------|-----|
| fastapi | 0.104.1 | Framework web |
| uvicorn | 0.24.0 | Servidor ASGI |
| sqlalchemy | 2.0.23 | ORM |
| psycopg2-binary | 2.9.9 | Driver PostgreSQL |
| redis | 5.0.1 | Cliente Redis |
| pytest | 7.4.3 | Framework testing |
| bandit | 1.7.5 | Análisis de seguridad |

## 🚦 CI/CD Pipeline

El proyecto incluye un pipeline automatizado en GitHub Actions que ejecuta:

- ✅ Tests unitarios
- ✅ Tests de integración
- ✅ Tests del sistema
- 🔒 Análisis de seguridad (Bandit)

Ver `.github/workflows/ci.yml` para más detalles.
