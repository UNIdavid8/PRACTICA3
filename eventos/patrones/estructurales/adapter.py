from eventos.entidades import Servicio
from .composite import ComponenteServicio


class APIExternaStreaming:
    def fetch_stream_data(self, resolution: str) -> dict:
        return {"tier": resolution, "cost_usd": 600.0 if resolution == "4K" else 200.0}


class ProveedorStreamingAdapter(ComponenteServicio):
    def __init__(self, resolucion: str):
        self.api = APIExternaStreaming()
        self.resolucion = resolucion

    def obtener_servicio(self) -> Servicio:
        datos = self.api.fetch_stream_data(self.resolucion)
        return Servicio(
            nombre=f"Streaming {datos['tier']}",
            descripcion="Integración vía API de terceros",
            precio=datos["cost_usd"],
        )