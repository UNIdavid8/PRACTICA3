from ..creacionales.factory import ServicioFactory

class PaqueteServicios:
    def __init__(self, nombre):
        self.nombre = nombre
        self.servicios = []

    def agregar(self, servicio):
        self.servicios.append(servicio)

    def obtener_coste_total(self):
        return sum(s.coste for s in self.servicios)

    def obtener_servicio(self):
        return ServicioFactory.crear(self.nombre, "Paquete Composite", self.obtener_coste_total())