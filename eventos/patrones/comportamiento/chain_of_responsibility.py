from abc import ABC, abstractmethod


class ManejadorValidacion(ABC):
    def __init__(self):
        self.siguiente = None

    def set_siguiente(self, manejador):
        self.siguiente = manejador
        return manejador

    @abstractmethod
    def validar(self, evento) -> tuple[bool, str]:
        if self.siguiente:
            return self.siguiente.validar(evento)
        return True, "Validación exitosa"


class ValidarFecha(ManejadorValidacion):
    def validar(self, evento):
        if not evento.fecha:
            return False, "[Error] El evento carece de fecha programada."
        return super().validar(evento)


class ValidarCapacidad(ManejadorValidacion):
    def validar(self, evento):
        if evento.ubicacion and evento.ubicacion.capacidad < 50:
            return (
                False,
                "[Error] La capacidad de la ubicación es inferior al mínimo exigido (50).",
            )
        return super().validar(evento)