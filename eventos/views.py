from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import random

from .memoria import db_eventos, guardar_evento, obtener_evento
from .entidades import Ubicacion
from .patrones.creacionales.singleton import ConfiguracionGlobal
from .patrones.creacionales.builder import (
    DirectorEvento,
    EventoConferenciaBuilder,
    EventoBodaBuilder,
    EventoConciertoBuilder,
    EventoCenaEmpresaBuilder,
)

# Patrones ya usados de práctica anterior
from .patrones.practica2 import (
    ValidarFecha,
    ValidarCapacidad,
    AbstraccionRepresentacion,
    ExportadorHTML,
    ExportadorAPIJSON,
)

# Actividad 3
from .patrones.estructurales.decorator import (
    EventoBase,
    MusicaEnVivoDecorator,
    CateringPremiumDecorator,
    SeguridadVIPDecorator,
    StreamingAvanzadoDecorator,
)
from .patrones.comportamiento.observer import (
    NotificadorEmail,
    NotificadorProveedor,
    NotificadorAnalytics,
)
from .patrones.comportamiento.template_method import (
    ProcesoConferencia,
    ProcesoBoda,
    ProcesoConcierto,
)


def panel_principal(request):
    """Vista principal con Bridge y panel de notificaciones/logs."""
    config = ConfiguracionGlobal()
    lista_eventos = list(db_eventos.values())

    # Bridge: salida HTML o JSON
    if request.GET.get("export") == "json":
        bridge = AbstraccionRepresentacion(ExportadorAPIJSON())
        salida = bridge.procesar(lista_eventos)
        return JsonResponse(salida, safe=False)

    bridge = AbstraccionRepresentacion(ExportadorHTML())
    salida = bridge.procesar(lista_eventos)

    contexto = salida["contexto"]
    contexto.update(
        {
            "moneda": config.moneda,
            "impuestos": config.impuestos,
            # Observer / Template logs persistidos en sesión
            "notificaciones": request.session.pop("notificaciones", []),
            "logs_template": request.session.pop("logs_template", []),
            # Resumen Decorator
            "resumen_extras": request.session.pop("resumen_extras", None),
        }
    )
    return render(request, "eventos/dashboard.html", contexto)


def crear_evento_builder(request, tipo):
    """Creación con Builder + CoR + Template Method + Decorator + Observer."""
    director = DirectorEvento()
    ubicacion_estandar = Ubicacion("Recinto Principal", "Av. Universidad 1", 500)

    # Builder
    if tipo == "conferencia":
        director.builder = EventoConferenciaBuilder()
        director.construir_conferencia_estandar(
            f"Conf_{random.randint(100, 999)}", "2026-06-01", ubicacion_estandar
        )
    elif tipo == "boda":
        director.builder = EventoBodaBuilder()
        director.construir_boda_clasica(
            f"Boda_{random.randint(100, 999)}", "2026-07-15", ubicacion_estandar
        )
    elif tipo == "concierto":
        director.builder = EventoConciertoBuilder()
        director.construir_concierto_rock(
            f"Live_{random.randint(100, 999)}", "2026-09-20", ubicacion_estandar
        )
    elif tipo == "cena":
        director.builder = EventoCenaEmpresaBuilder()
        director.construir_cena_navidad(
            f"Cena_{random.randint(100, 999)}", "2026-12-15", ubicacion_estandar
        )
    else:
        return HttpResponse("Tipo de evento no soportado.", status=400)

    evento_nuevo = director.builder.get_resultado()

    # Chain of Responsibility (ya existente)
    pipeline_validacion = ValidarFecha()
    pipeline_validacion.set_siguiente(ValidarCapacidad())
    es_valido, mensaje_error = pipeline_validacion.validar(evento_nuevo)
    if not es_valido:
        return HttpResponse(
            f"Generación abortada por Chain of Responsibility: {mensaje_error}",
            status=400,
        )

    # ---------------------------
    # TEMPLATE METHOD (Actividad 3)
    # ---------------------------
    proceso = None
    if tipo == "conferencia":
        proceso = ProcesoConferencia()
    elif tipo == "boda":
        proceso = ProcesoBoda()
    elif tipo == "concierto":
        proceso = ProcesoConcierto()

    if proceso:
        resultado_template = proceso.ejecutar(
            {
                "nombre": evento_nuevo.nombre,
                "fecha": evento_nuevo.fecha,
                "coste_base": 1000.0,
                # Si quieres, aquí puedes pasar campos concretos según tipo
                "ponentes": ["Ponente 1", "Ponente 2"] if tipo == "conferencia" else [],
            }
        )
        request.session["logs_template"] = resultado_template["log"]
    else:
        request.session["logs_template"] = [
            "1) Datos validados",
            "2) Servicios base configurados",
            "3) Costes calculados",
            "4) Evento confirmado",
        ]

    # ---------------------------
    # DECORATOR (Actividad 3)
    # ---------------------------
    # Extras por query params:
    # /crear/conferencia/?musica=1&catering=1&vip=1&streaming=1
    evento_coste = EventoBase(evento_nuevo.nombre, 1000.0)
    extras_aplicados = []

    if request.GET.get("musica") == "1":
        evento_coste = MusicaEnVivoDecorator(evento_coste)
        extras_aplicados.append("Música en vivo")
    if request.GET.get("catering") == "1":
        evento_coste = CateringPremiumDecorator(evento_coste)
        extras_aplicados.append("Catering premium")
    if request.GET.get("vip") == "1":
        evento_coste = SeguridadVIPDecorator(evento_coste)
        extras_aplicados.append("Seguridad VIP")
    if request.GET.get("streaming") == "1":
        evento_coste = StreamingAvanzadoDecorator(evento_coste)
        extras_aplicados.append("Streaming avanzado")

    request.session["resumen_extras"] = {
        "descripcion": evento_coste.get_descripcion(),
        "coste_total": evento_coste.get_coste(),
        "extras": extras_aplicados,
    }

    # ---------------------------
    # OBSERVER (Actividad 3)
    # ---------------------------
    # Necesitas en Evento: atributo estado y método crear_observable()
    try:
        observable = evento_nuevo.crear_observable()

        email = NotificadorEmail()
        proveedor = NotificadorProveedor()
        analytics = NotificadorAnalytics()

        observable.agregar_observador(email)
        observable.agregar_observador(proveedor)
        observable.agregar_observador(analytics)

        observable.cambiar_estado("confirmado")

        request.session["notificaciones"] = (
            email.historial + proveedor.historial + analytics.historial
        )
    except Exception:
        # Fallback por si todavía no añadiste crear_observable/estado en Evento
        request.session["notificaciones"] = [
            f"[INFO] Evento '{evento_nuevo.nombre}' creado (pendiente de integración completa de Observer)."
        ]

    guardar_evento(evento_nuevo)
    return redirect("panel_principal")


def clonar_evento_prototype(request, evento_id):
    evento_original = obtener_evento(evento_id)
    if not evento_original:
        return HttpResponse("Error: Evento no encontrado.", status=404)

    evento_clonado = evento_original.clonar()
    evento_clonado.nombre = f"Copia de {evento_original.nombre}"
    guardar_evento(evento_clonado)
    return redirect("panel_principal")


def panel_configuracion(request):
    config = ConfiguracionGlobal()
    if config.moneda == "EUR":
        config.actualizar_configuracion(moneda="USD", impuestos=10.0)
    else:
        config.actualizar_configuracion(moneda="EUR", impuestos=21.0)
    return redirect("panel_principal")