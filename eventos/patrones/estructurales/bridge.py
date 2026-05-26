class AbstraccionRepresentacion:
    def __init__(self, implementador): self.implementador = implementador
    def procesar(self, eventos): return self.implementador.exportar(eventos)

class ExportadorHTML:
    def exportar(self, eventos): return {"contexto": {"eventos": eventos}}

class ExportadorAPIJSON:
    def exportar(self, eventos):
        return [{"id": e.id, "nombre": e.nombre, "fecha": e.fecha, "tipo": e.tipo} for e in eventos]