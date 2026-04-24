from abc import ABC, abstractmethod
from eventos.entidades import Servicio


class ComponenteServicio(ABC):
    @abstractmethod
    def obtener_servicio(self) -> Servicio:
        pass


class PaqueteServicios(ComponenteServicio):
    """Permite tratar grupos de servicios como un único servicio unificado."""

    def __init__(self, nombre: str):
        self.nombre = nombre
        self.hijos = []

    def agregar(self, servicio: Servicio):
        self.hijos.append(servicio)

    def obtener_servicio(self) -> Servicio:
        precio_total = sum([s.precio for s in self.hijos]) * 0.85
        descripcion_combinada = " + ".join([s.nombre for s in self.hijos])
        return Servicio(f"Pack: {self.nombre}", descripcion_combinada, precio_total)