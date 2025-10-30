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

 🏗️ Estructura del Proyecto

app/
├── init.py
├── main.py
├── db.py
├── models.py
├── schemas.py
├── crud.py
└── routers/
├── empleados.py
└── proyectos.py
.env.example
.gitignore


⚖️ Reglas de negocio implementadas

✅ Regla 1: Un empleado no puede eliminarse si es gerente de algún proyecto activo.
✅ Regla 2: Los nombres de los proyectos deben ser únicos.
✅ Regla 3: Un empleado no puede asignarse dos veces al mismo proyecto.
✅ Regla 4: Si se elimina un proyecto, se eliminan sus asignaciones (manejadas por SQLModel).
✅ Regla 5: Los filtros GET permiten consultar por estado y presupuesto.

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

Método    Endpoint	                                       Descripción
POST	  /empleados                                      /	Crear nuevo empleado
GET	    /empleados                                      /	Listar empleados (filtros: especialidad, estado)
GET	    /empleados                                      /{id}	Obtener empleado y proyectos asociados
PUT	    /empleados                                      /{id}	Actualizar datos del empleado
DELETE	/empleados                                      /{id}	Eliminar empleado (si no es gerente activo)
GET	    /empleados/{id}                                 /proyectos	Listar proyectos donde trabaja un empleado

Autor 
Yeferson Guaca
