from abc import ABC, abstractmethod


class ImplementacionExportacion(ABC):
    @abstractmethod
    def exportar(self, datos) -> dict:
        pass


class ExportadorHTML(ImplementacionExportacion):
    def exportar(self, datos):
        return {"formato": "html", "contexto": {"eventos": datos}}


class ExportadorAPIJSON(ImplementacionExportacion):
    def exportar(self, datos):
        payload = [
            {"id": e.id, "nombre": e.nombre, "tipo": e.tipo, "fecha": e.fecha}
            for e in datos
        ]
        return {"formato": "json", "data": payload}


class AbstraccionRepresentacion:
    def __init__(self, implementacion: ImplementacionExportacion):
        self.implementacion = implementacion

    def procesar(self, eventos):
        return self.implementacion.exportar(eventos)