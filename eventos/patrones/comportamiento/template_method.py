class ProcesoEventoTemplate:
    def ejecutar(self, datos):
        log = []
        log.append(self.validar(datos))
        log.append(self.configurar(datos))
        log.append(self.calcular(datos))
        return {"log": log}
    def validar(self, datos): return "Validación genérica completada"
    def configurar(self, datos): return "Configuración genérica completada"
    def calcular(self, datos): return "Costes genéricos calculados"

class ProcesoConferencia(ProcesoEventoTemplate):
    def configurar(self, datos): return f"Conferencia configurada con {len(datos.get('ponentes', []))} ponentes"

class ProcesoBoda(ProcesoEventoTemplate):
    def configurar(self, datos): return "Boda configurada con protocolo nupcial"

class ProcesoConcierto(ProcesoEventoTemplate):
    def configurar(self, datos): return "Concierto configurado con pruebas de sonido"