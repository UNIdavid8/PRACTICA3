class ValidadorBase:
    def __init__(self): self.siguiente = None
    def set_siguiente(self, validador):
        self.siguiente = validador
        return validador
    def validar(self, evento):
        if self.siguiente: return self.siguiente.validar(evento)
        return True, ""

class ValidarFecha(ValidadorBase):
    def validar(self, evento):
        if not evento.fecha: return False, "Fecha inválida"
        return super().validar(evento)

class ValidarCapacidad(ValidadorBase):
    def validar(self, evento):
        if evento.ubicacion and evento.ubicacion.capacidad < 10: return False, "Capacidad insuficiente"
        return super().validar(evento)