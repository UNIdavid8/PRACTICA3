from eventos.patrones.comportamiento.template_method import (
    ProcesoConferencia,
    ProcesoBoda,
    ProcesoConcierto,
)


def test_template_conferencia():
    proceso = ProcesoConferencia()
    resultado = proceso.ejecutar(
        {"nombre": "Conf Python", "fecha": "2026-09-20", "coste_base": 1000, "ponentes": ["A", "B"]}
    )
    assert resultado["ok"] is True
    assert resultado["tipo"] == "conferencia"
    assert resultado["coste_total"] == 1300.0
    assert len(resultado["log"]) >= 4


def test_template_boda_y_concierto():
    boda = ProcesoBoda().ejecutar({"nombre": "Boda Ana", "fecha": "2026-05-10", "coste_base": 5000})
    concierto = ProcesoConcierto().ejecutar({"nombre": "Rock Fest", "fecha": "2026-08-01", "coste_base": 7000})

    assert boda["coste_total"] == 7000.0
    assert concierto["coste_total"] == 10500.0