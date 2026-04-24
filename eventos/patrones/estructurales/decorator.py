from abc import ABC, abstractmethod


class EventoComponent(ABC):
    @abstractmethod
    def get_descripcion(self) -> str:
        pass

    @abstractmethod
    def get_coste(self) -> float:
        pass


class EventoBase(EventoComponent):
    def __init__(self, nombre: str, coste_base: float):
        self.nombre = nombre
        self.coste_base = coste_base

    def get_descripcion(self) -> str:
        return f"Evento: {self.nombre}"

    def get_coste(self) -> float:
        return self.coste_base


class EventoDecorator(EventoComponent):
    def __init__(self, evento: EventoComponent):
        self._evento = evento

    def get_descripcion(self) -> str:
        return self._evento.get_descripcion()

    def get_coste(self) -> float:
        return self._evento.get_coste()


class MusicaEnVivoDecorator(EventoDecorator):
    def get_descripcion(self) -> str:
        return f"{super().get_descripcion()} + Música en vivo"

    def get_coste(self) -> float:
        return super().get_coste() + 500.0


class CateringPremiumDecorator(EventoDecorator):
    def get_descripcion(self) -> str:
        return f"{super().get_descripcion()} + Catering premium"

    def get_coste(self) -> float:
        return super().get_coste() + 1200.0


class SeguridadVIPDecorator(EventoDecorator):
    def get_descripcion(self) -> str:
        return f"{super().get_descripcion()} + Seguridad VIP"

    def get_coste(self) -> float:
        return super().get_coste() + 800.0


class StreamingAvanzadoDecorator(EventoDecorator):
    def get_descripcion(self) -> str:
        return f"{super().get_descripcion()} + Streaming avanzado"

    def get_coste(self) -> float:
        return super().get_coste() + 600.0