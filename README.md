🚀 Sistema de Gestión de Proyectos

API REST desarrollada con **FastAPI** y **SQLModel**, que permite gestionar empleados y proyectos dentro de una organización.  
Incluye relaciones 1:N y N:M, validaciones con **Pydantic**, manejo de errores HTTP, y reglas de negocio específicas.

---

📦 Características principales

✅ CRUD completo para **Empleados** y **Proyectos**  
✅ Asignación y desasignación de empleados a proyectos (relación N:M)  
✅ Asignación de **gerente único por proyecto** (relación 1:N)  
✅ Validaciones automáticas con **Pydantic**  
✅ Filtros en consultas GET  
✅ Manejo de errores HTTP (400, 404, 409, 500)  
✅ Documentación interactiva con **Swagger UI**  
✅ Arquitectura modular (routers, crud, schemas, models, db)  
✅ Compatible con variables de entorno `.env.example`  

---


🧩 Tecnologías usadas

| Tecnología   | Descripción                         |
| ------------ | ----------------------------------- |
| **FastAPI**  | Framework web moderno y asíncrono   |
| **SQLModel** | ORM basado en SQLAlchemy y Pydantic |
| **Pydantic** | Validación de datos y esquemas      |
| **SQLite**   | Base de datos ligera por defecto    |
| **Uvicorn**  | Servidor ASGI de alto rendimiento   |


⚠️ Manejo de errores HTTP
Código	Motivo
200	Solicitud exitosa
201	Creación exitosa
400	Datos inválidos o malformados
404	Recurso no encontrado
409	Conflicto (duplicados, restricciones de negocio)
500	Error interno del servidor

📚 Endpoints principales

🧍‍♂️ Empleados

| Método     | Endpoint                    | Descripción                                          |
| ---------- | --------------------------- | ---------------------------------------------------- |
| **POST**   | `/empleados/`               | Crear nuevo empleado                                 |
| **GET**    | `/empleados/`               | Listar empleados (filtros: `especialidad`, `estado`) |
| **GET**    | `/empleados/{id}`           | Obtener empleado y proyectos asociados               |
| **PUT**    | `/empleados/{id}`           | Actualizar datos del empleado                        |
| **DELETE** | `/empleados/{id}`           | Eliminar empleado (si no es gerente activo)          |
| **GET**    | `/empleados/{id}/proyectos` | Listar proyectos donde trabaja un empleado           |



🏗️ Proyectos


| Método     | Endpoint                                   | Descripción                                         |
| ---------- | ------------------------------------------ | --------------------------------------------------- |
| **POST**   | `/proyectos/`                              | Crear nuevo proyecto (único nombre)                 |
| **GET**    | `/proyectos/`                              | Listar proyectos (filtros: `estado`, `presupuesto`) |
| **GET**    | `/proyectos/{id}`                          | Obtener proyecto, gerente y empleados               |
| **PUT**    | `/proyectos/{id}`                          | Actualizar información de proyecto                  |
| **DELETE** | `/proyectos/{id}`                          | Eliminar proyecto                                   |
| **POST**   | `/proyectos/{id}/asignar`                  | Asignar empleado a proyecto                         |
| **DELETE** | `/proyectos/{id}/desasignar/{empleado_id}` | Desasignar empleado de proyecto                     |
| **PUT**    | `/proyectos/{id}/gerente/{empleado_id}`    | Asignar o cambiar gerente del proyecto              |
| **GET**    | `/proyectos/{id}/empleados`                | Listar empleados del proyecto                       |


Autor 
Yeferson Guaca

