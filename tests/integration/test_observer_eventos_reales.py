from dataclasses import dataclass
from eventos.patrones.comportamiento.observer import EventoObservable, NotificadorEmail


@dataclass
class EventoRealMinimo:
    nombre: str
    fecha: str
    estado: str = "activo"


def test_observer_con_evento_real():
    evento = EventoRealMinimo("Evento Real", "2026-12-01")
    observable = EventoObservable(evento)
    email = NotificadorEmail()
    observable.agregar_observador(email)

    observable.cambiar_fecha("2026-12-15")
    assert len(email.historial) == 1