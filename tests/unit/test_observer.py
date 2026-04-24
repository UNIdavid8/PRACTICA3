from dataclasses import dataclass
from eventos.patrones.comportamiento.observer import (
    EventoObservable,
    NotificadorEmail,
    NotificadorProveedor,
    NotificadorAnalytics,
)


@dataclass
class EventoFake:
    nombre: str
    fecha: str
    estado: str = "activo"


def test_observer_notifica_a_todos():
    evento = EventoFake("Conferencia IA", "2026-06-10")
    observable = EventoObservable(evento)

    email = NotificadorEmail()
    prov = NotificadorProveedor()
    analytics = NotificadorAnalytics()

    observable.agregar_observador(email)
    observable.agregar_observador(prov)
    observable.agregar_observador(analytics)

    observable.cambiar_estado("aplazado")

    assert len(email.historial) == 1
    assert len(prov.historial) == 1
    assert len(analytics.historial) == 1


def test_observer_eliminar_observador():
    evento = EventoFake("Concierto X", "2026-07-01")
    observable = EventoObservable(evento)

    email = NotificadorEmail()
    prov = NotificadorProveedor()

    observable.agregar_observador(email)
    observable.agregar_observador(prov)
    observable.eliminar_observador(prov)

    observable.cancelar_evento()

    assert len(email.historial) == 1
    assert len(prov.historial) == 0