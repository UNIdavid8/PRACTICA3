import random
from eventos.models import Ubicacion
from ..creacionales.builder import DirectorEvento, EventoConferenciaBuilder, EventoBodaBuilder, EventoConciertoBuilder, EventoCenaEmpresaBuilder
from ..comportamiento.chain_of_responsibility import ValidarFecha, ValidarCapacidad
from ..comportamiento.template_method import ProcesoConferencia, ProcesoBoda, ProcesoConcierto
from ..estructurales.decorator import EventoBase, MusicaEnVivoDecorator, CateringPremiumDecorator, SeguridadVIPDecorator, StreamingAvanzadoDecorator
from ..comportamiento.observer import NotificadorEmail, NotificadorProveedor, NotificadorAnalytics

class EventoFacade:
    def procesar_creacion(self, tipo, request_get):
        director = DirectorEvento()
        ubicacion, _ = Ubicacion.objects.get_or_create(nombre="Recinto", defaults={"direccion": "Av 1", "capacidad": 500})
        if tipo == "conferencia":
            director.builder = EventoConferenciaBuilder()
            director.construir_conferencia_estandar(f"Conf_{random.randint(10,99)}", "2026-06-01", ubicacion)
        elif tipo == "boda":
            director.builder = EventoBodaBuilder()
            director.construir_boda_clasica(f"Boda_{random.randint(10,99)}", "2026-07-15", ubicacion)
        elif tipo == "concierto":
            director.builder = EventoConciertoBuilder()
            director.construir_concierto_rock(f"Live_{random.randint(10,99)}", "2026-09-20", ubicacion)
        elif tipo == "cena":
            director.builder = EventoCenaEmpresaBuilder()
            director.construir_cena_navidad(f"Cena_{random.randint(10,99)}", "2026-12-15", ubicacion)
        else:
            return False, "Tipo no soportado", [], {}, []

        evento = director.builder.get_resultado()
        pipeline = ValidarFecha()
        pipeline.set_siguiente(ValidarCapacidad())
        valido, msg = pipeline.validar(evento)
        if not valido: return False, msg, [], {}, []

        evento.save()
        for s in evento.servicios_temporales:
            s.evento = evento
            s.save()

        proceso = ProcesoConferencia() if tipo == "conferencia" else ProcesoBoda() if tipo == "boda" else ProcesoConcierto() if tipo == "concierto" else None
        logs = proceso.ejecutar({"nombre": evento.nombre, "fecha": evento.fecha, "ponentes": ["A", "B"]})["log"] if proceso else ["Proceso estándar completado"]

        evento_coste = EventoBase(evento.nombre, 1000.0)
        extras = []
        if request_get.get("musica") == "1":
            evento_coste = MusicaEnVivoDecorator(evento_coste)
            extras.append("Música")
        if request_get.get("catering") == "1":
            evento_coste = CateringPremiumDecorator(evento_coste)
            extras.append("Catering")
        if request_get.get("vip") == "1":
            evento_coste = SeguridadVIPDecorator(evento_coste)
            extras.append("VIP")
        if request_get.get("streaming") == "1":
            evento_coste = StreamingAvanzadoDecorator(evento_coste)
            extras.append("Streaming")

        resumen_extras = {"descripcion": evento_coste.get_descripcion(), "coste_total": evento_coste.get_coste(), "extras": extras}

        observable = evento.crear_observable()
        em = NotificadorEmail()
        pr = NotificadorProveedor()
        an = NotificadorAnalytics()
        observable.agregar_observador(em)
        observable.agregar_observador(pr)
        observable.agregar_observador(an)
        observable.cambiar_estado("confirmado")
        notif = em.historial + pr.historial + an.historial

        return True, "", logs, resumen_extras, notif