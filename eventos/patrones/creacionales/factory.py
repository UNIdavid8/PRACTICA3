from eventos.models import Servicio

class ServicioFactory:
    @staticmethod
    def crear(nombre, descripcion, coste):
        return Servicio(nombre=nombre, descripcion=descripcion, coste=coste)