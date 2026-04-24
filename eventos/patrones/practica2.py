from abc import ABC, abstractmethod
from eventos.entidades import Servicio

#COMPOSITE

class ComponenteServicio(ABC):
    @abstractmethod
    def obtener_servicio(self) -> Servicio: pass

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

#ADAPTER

class APIExternaStreaming:
    """Simula una API de terceros con estructuras de datos incompatibles."""
    def fetch_stream_data(self, resolution: str) -> dict:
        return {"tier": resolution, "cost_usd": 600.0 if resolution == "4K" else 200.0}

class ProveedorStreamingAdapter(ComponenteServicio):
    """Adapta la respuesta de la API externa al modelo interno 'Servicio'."""
    def __init__(self, resolucion: str):
        self.api = APIExternaStreaming()
        self.resolucion = resolucion
        
    def obtener_servicio(self) -> Servicio:
        datos = self.api.fetch_stream_data(self.resolucion)
        return Servicio(
            nombre=f"Streaming Externo ({datos['tier']})",
            descripcion="Integración vía API de terceros",
            precio=datos['cost_usd']
        )

#CHAIN OF RESPONSIBILITY

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
            return False, "[Error] La capacidad de la ubicación es inferior al mínimo exigido (50)."
        return super().validar(evento)

#BRIDGE

class ImplementacionExportacion(ABC):
    @abstractmethod
    def exportar(self, datos) -> dict: pass

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