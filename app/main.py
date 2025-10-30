from fastapi import FastAPI
from app.db import init_db
from app.routers import empleados, proyectos
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Request
from starlette.status import HTTP_400_BAD_REQUEST

app = FastAPI(title="Sistema de Gestión de Proyectos", version="2.0")

init_db()

app.include_router(empleados.router, prefix="/empleados", tags=["Empleados"])
app.include_router(proyectos.router, prefix="/proyectos", tags=["Proyectos"])

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={"error": "Bad Request", "detail": exc.errors(), "body": exc.body}
    )
