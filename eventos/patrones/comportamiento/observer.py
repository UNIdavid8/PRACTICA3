class EventoObservable:
    def __init__(self, evento):
        self.evento = evento
        self.observadores = []
    def agregar_observador(self, obs):
        if obs not in self.observadores: self.observadores.append(obs)
    def notificar(self):
        for obs in self.observadores: obs.actualizar(self.evento)
    def cambiar_estado(self, estado):
        self.evento.estado_actual = estado
        self.evento.save()
        self.notificar()

class NotificadorEmail:
    def __init__(self): self.historial = []
    def actualizar(self, evento): self.historial.append(f"Email: {evento.nombre} es ahora {evento.estado_actual}")

class NotificadorProveedor:
    def __init__(self): self.historial = []
    def actualizar(self, evento): self.historial.append(f"Proveedor: {evento.nombre} modificado")

class NotificadorAnalytics:
    def __init__(self): self.historial = []
    def actualizar(self, evento): self.historial.append(f"Analytics: Registro de {evento.nombre}")