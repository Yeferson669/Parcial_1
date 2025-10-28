from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_proyecto_y_asignaciones():
    # crear gerente
    r = client.post("/empleados/", json={"nombre":"Jorge","especialidad":"Gerencia","salario":2000,"estado":"ACTIVO"})
    assert r.status_code == 201
    gid = r.json()["id"]

    # crear otro empleado
    r2 = client.post("/empleados/", json={"nombre":"Luis","especialidad":"Dev","salario":1500,"estado":"ACTIVO"})
    eid = r2.json()["id"]

    # crear proyecto con gerente
    r3 = client.post("/proyectos/", json={"nombre":"ProyectoTest","descripcion":"desc","presupuesto":5000,"estado":"PLANEADO","gerente_id":gid})
    assert r3.status_code == 201
    pid = r3.json()["id"]

    # asignar empleado
    r4 = client.post(f"/proyectos/{pid}/asignaciones", json={"empleado_id":eid})
    assert r4.status_code == 201

    # asignación duplicada -> 409
    r5 = client.post(f"/proyectos/{pid}/asignaciones", json={"empleado_id":eid})
    assert r5.status_code == 409

    # intentar eliminar gerente -> 409
    r6 = client.delete(f"/empleados/{gid}")
    assert r6.status_code == 409

    # eliminar proyecto
    r7 = client.delete(f"/proyectos/{pid}")
    assert r7.status_code == 204

    # ahora eliminar gerente debería funcionar (ya no tiene proyectos)
    r8 = client.delete(f"/empleados/{gid}")
    assert r8.status_code == 204
