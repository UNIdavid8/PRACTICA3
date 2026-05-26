from ..creacionales.factory import ServicioFactory

class APIExternaStreaming:
    def conectar_servidor_rtmp(self, calidad):
        return {"status": 200, "bandwidth": calidad, "price": 100.0}

class ProveedorStreamingAdapter:
    def __init__(self, calidad):
        self.api = APIExternaStreaming()
        self.calidad = calidad

    def obtener_servicio(self):
        respuesta = self.api.conectar_servidor_rtmp(self.calidad)
        return ServicioFactory.crear(f"Streaming {self.calidad}", "Transmisión externa", respuesta["price"])