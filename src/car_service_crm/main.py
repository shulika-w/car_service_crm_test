"""Точка входу FastAPI-додатку: реєстрація роутерів, конфігурація OpenAPI, запуск серверу."""

from fastapi import FastAPI
from .routers import users as users_router
from .routers import cars as cars_router
from .routers import services as services_router
from .routers import mechanics as mechanics_router
from .routers import documents as documents_router
from .routers import appointments as appointments_router
from fastapi.openapi.utils import get_openapi

# Створення таблиць (до запуску app)
from .db import Base, engine
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Car Service CRM",
    description="API для управління записами на обслуговування автомобілів для СТО",
    version="0.1.0"
)

@app.get("/")
def read_root():
    return {"message": "API is working!"}

app.include_router(users_router.router)
app.include_router(cars_router.router)
app.include_router(services_router.router)
app.include_router(mechanics_router.router)
app.include_router(documents_router.router)
app.include_router(appointments_router.router)

# Додаємо Bearer Auth як окремий security scheme
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"]["BearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", []).append({"BearerAuth": []})
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi