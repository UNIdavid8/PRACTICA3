class EventoBase:
    def __init__(self, descripcion, coste):
        self.descripcion = descripcion
        self.coste = coste
    def get_descripcion(self): return self.descripcion
    def get_coste(self): return self.coste

class DecoradorEvento:
    def __init__(self, componente): self.componente = componente
    def get_descripcion(self): return self.componente.get_descripcion()
    def get_coste(self): return self.componente.get_coste()

class MusicaEnVivoDecorator(DecoradorEvento):
    def get_descripcion(self): return super().get_descripcion() + " + Música"
    def get_coste(self): return super().get_coste() + 500.0

class CateringPremiumDecorator(DecoradorEvento):
    def get_descripcion(self): return super().get_descripcion() + " + Catering Premium"
    def get_coste(self): return super().get_coste() + 800.0

class SeguridadVIPDecorator(DecoradorEvento):
    def get_descripcion(self): return super().get_descripcion() + " + Seguridad VIP"
    def get_coste(self): return super().get_coste() + 1000.0

class StreamingAvanzadoDecorator(DecoradorEvento):
    def get_descripcion(self): return super().get_descripcion() + " + Streaming Avanzado"
    def get_coste(self): return super().get_coste() + 300.0