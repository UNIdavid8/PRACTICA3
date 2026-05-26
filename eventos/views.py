from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Evento
from .patrones.creacionales.singleton import ConfiguracionGlobal
from .patrones.estructurales.facade import EventoFacade
from .patrones.estructurales.bridge import AbstraccionRepresentacion, ExportadorHTML, ExportadorAPIJSON

def panel_principal(request):
    config = ConfiguracionGlobal()
    lista_eventos = list(Evento.objects.all())

    if request.GET.get("export") == "json":
        bridge = AbstraccionRepresentacion(ExportadorAPIJSON())
        return JsonResponse(bridge.procesar(lista_eventos), safe=False)

    bridge = AbstraccionRepresentacion(ExportadorHTML())
    contexto = bridge.procesar(lista_eventos)["contexto"]

    contexto.update({
        "moneda": config.moneda,
        "impuestos": getattr(config, 'impuestos', 21.0),
        "notificaciones": request.session.pop("notificaciones", []),
        "logs_template": request.session.pop("logs_template", []),
        "resumen_extras": request.session.pop("resumen_extras", None),
    })
    return render(request, "eventos/dashboard.html", contexto)

def crear_evento_builder(request, tipo):
    facade = EventoFacade()
    exito, msg, logs, extras, notif = facade.procesar_creacion(tipo, request.GET)
    if not exito: return HttpResponse(msg, status=400)
    request.session["logs_template"] = logs
    request.session["resumen_extras"] = extras
    request.session["notificaciones"] = notif
    return redirect("panel_principal")

def clonar_evento_prototype(request, evento_id):
    try:
        evento = Evento.objects.get(id=evento_id)
        evento.clonar()
    except Evento.DoesNotExist:
        return HttpResponse("Error", status=404)
    return redirect("panel_principal")

def panel_configuracion(request):
    config = ConfiguracionGlobal()
    if config.moneda == "EUR":
        config.actualizar_configuracion(moneda="USD", impuestos=10.0)
    else:
        config.actualizar_configuracion(moneda="EUR", impuestos=21.0)
    return redirect("panel_principal")