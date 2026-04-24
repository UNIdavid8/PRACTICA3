from abc import ABC, abstractmethod


class ProcesoCreacionEvento(ABC):
    def ejecutar(self, datos: dict) -> dict:
        log = []
        self.validar_datos(datos, log)
        self.configurar_servicios(datos, log)
        coste = self.calcular_costes(datos, log)
        self.confirmar_evento(datos, coste, log)
        return {"ok": True, "coste_total": coste, "log": log, "tipo": self.tipo_evento()}

    def validar_datos(self, datos, log):
        if not datos.get("nombre"):
            raise ValueError("El evento debe tener nombre.")
        if not datos.get("fecha"):
            raise ValueError("El evento debe tener fecha.")
        log.append("1) Datos validados")

    def configurar_servicios(self, datos, log):
        log.append("2) Servicios base configurados")
        self.configuracion_especifica(datos, log)

    def calcular_costes(self, datos, log):
        base = float(datos.get("coste_base", 0))
        extra = self.coste_especifico(datos, log)
        total = base + extra
        log.append(f"3) Costes calculados: base={base}, extra={extra}, total={total}")
        return total

    def confirmar_evento(self, datos, coste, log):
        log.append(f"4) Evento confirmado: {datos['nombre']} (coste total: {coste})")

    @abstractmethod
    def configuracion_especifica(self, datos, log):
        pass

    @abstractmethod
    def coste_especifico(self, datos, log) -> float:
        pass

    @abstractmethod
    def tipo_evento(self) -> str:
        pass


class ProcesoConferencia(ProcesoCreacionEvento):
    def configuracion_especifica(self, datos, log):
        ponentes = datos.get("ponentes", [])
        log.append(f"   - Configuración conferencia: ponentes={len(ponentes)}")

    def coste_especifico(self, datos, log) -> float:
        ponentes = len(datos.get("ponentes", []))
        return ponentes * 150.0

    def tipo_evento(self) -> str:
        return "conferencia"


class ProcesoBoda(ProcesoCreacionEvento):
    def configuracion_especifica(self, datos, log):
        log.append("   - Configuración boda: ceremonia incluida")

    def coste_especifico(self, datos, log) -> float:
        return 2000.0

    def tipo_evento(self) -> str:
        return "boda"


class ProcesoConcierto(ProcesoCreacionEvento):
    def configuracion_especifica(self, datos, log):
        log.append("   - Configuración concierto: escenario y rider técnico")

    def coste_especifico(self, datos, log) -> float:
        return 3500.0

    def tipo_evento(self) -> str:
        return "concierto"