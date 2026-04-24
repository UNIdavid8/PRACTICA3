from eventos.entidades import Servicio
from patrones.composite import ComponenteServicio


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
            precio=datos["cost_usd"],
        )