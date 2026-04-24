from abc import ABC, abstractmethod


class Observador(ABC):
    @abstractmethod
    def actualizar(self, evento):
        pass


class EventoObservable:
    def __init__(self, evento):
        self._evento = evento
        self._observadores = []

    def agregar_observador(self, obs: Observador):
        if obs not in self._observadores:
            self._observadores.append(obs)

    def eliminar_observador(self, obs: Observador):
        if obs in self._observadores:
            self._observadores.remove(obs)

    def notificar(self):
        for obs in self._observadores:
            obs.actualizar(self._evento)

    def cambiar_fecha(self, nueva_fecha):
        self._evento.fecha = nueva_fecha
        self.notificar()

    def cambiar_estado(self, nuevo_estado):
        self._evento.estado = nuevo_estado
        self.notificar()

    def cancelar_evento(self):
        self._evento.estado = "cancelado"
        self.notificar()


class NotificadorEmail(Observador):
    def __init__(self):
        self.historial = []

    def actualizar(self, evento):
        self.historial.append(
            f"[EMAIL] Evento '{evento.nombre}' actualizado. Estado: {getattr(evento, 'estado', 'N/A')}, Fecha: {getattr(evento, 'fecha', 'N/A')}"
        )


class NotificadorProveedor(Observador):
    def __init__(self):
        self.historial = []

    def actualizar(self, evento):
        self.historial.append(
            f"[PROVEEDOR] Revisar cambios del evento '{evento.nombre}'."
        )


class NotificadorAnalytics(Observador):
    def __init__(self):
        self.historial = []

    def actualizar(self, evento):
        self.historial.append(
            f"[ANALYTICS] Cambio detectado en evento '{evento.nombre}'."
        )