from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import random

from .memoria import db_eventos, guardar_evento, obtener_evento
from .entidades import Ubicacion
from .patrones.creacionales.singleton import ConfiguracionGlobal
from .patrones.creacionales.builder import (
    DirectorEvento, EventoConferenciaBuilder, EventoBodaBuilder,
    EventoConciertoBuilder, EventoCenaEmpresaBuilder
)
# NUEVAS IMPORTACIONES
from .patrones.practica2 import (
    ValidarFecha, ValidarCapacidad, 
    AbstraccionRepresentacion, ExportadorHTML, ExportadorAPIJSON
)

def panel_principal(request):
    """Vista principal con patrón Bridge para servir HTML o API JSON."""
    config = ConfiguracionGlobal()
    lista_eventos = list(db_eventos.values())
    
    # Lógica Bridge: Desacopla la abstracción de la salida
    if request.GET.get('export') == 'json':
        bridge = AbstraccionRepresentacion(ExportadorAPIJSON())
        salida = bridge.procesar(lista_eventos)
        return JsonResponse(salida, safe=False)
    else:
        bridge = AbstraccionRepresentacion(ExportadorHTML())
        salida = bridge.procesar(lista_eventos)
        
        # Extendemos el contexto HTML con el Singleton
        contexto = salida["contexto"]
        contexto.update({'moneda': config.moneda, 'impuestos': config.impuestos})
        return render(request, 'eventos/dashboard.html', contexto)

def crear_evento_builder(request, tipo):
    """Creación con Builder y validación con Chain of Responsibility."""
    director = DirectorEvento()
    ubicacion_estandar = Ubicacion("Recinto Principal", "Av. Universidad 1", 500)
    
    if tipo == 'conferencia':
        director.builder = EventoConferenciaBuilder()
        director.construir_conferencia_estandar(f"Conf_{random.randint(100,999)}", "2026-06-01", ubicacion_estandar)
    elif tipo == 'boda':
        director.builder = EventoBodaBuilder()
        director.construir_boda_clasica(f"Boda_{random.randint(100,999)}", "2026-07-15", ubicacion_estandar)
    elif tipo == 'concierto':
        director.builder = EventoConciertoBuilder()
        director.construir_concierto_rock(f"Live_{random.randint(100,999)}", "2026-09-20", ubicacion_estandar)
    elif tipo == 'cena':
        director.builder = EventoCenaEmpresaBuilder()
        director.construir_cena_navidad(f"Cena_{random.randint(100,999)}", "2026-12-15", ubicacion_estandar)
    
    evento_nuevo = director.builder.get_resultado()

    # Lógica Chain of Responsibility: Validar antes de guardar
    pipeline_validacion = ValidarFecha()
    pipeline_validacion.set_siguiente(ValidarCapacidad())
    
    es_valido, mensaje_error = pipeline_validacion.validar(evento_nuevo)
    
    if not es_valido:
        return HttpResponse(f"Generación abortada por Chain of Responsibility: {mensaje_error}", status=400)

    guardar_evento(evento_nuevo)
    return redirect('panel_principal')

def clonar_evento_prototype(request, evento_id):
    evento_original = obtener_evento(evento_id)
    if not evento_original:
        return HttpResponse("Error: Evento no encontrado.", status=404)
    
    evento_clonado = evento_original.clonar()
    evento_clonado.nombre = f"Copia de {evento_original.nombre}"
    guardar_evento(evento_clonado)
    return redirect('panel_principal')

def panel_configuracion(request):
    config = ConfiguracionGlobal()
    if config.moneda == "EUR":
        config.actualizar_configuracion(moneda="USD", impuestos=10.0)
    else:
        config.actualizar_configuracion(moneda="EUR", impuestos=21.0)
    return redirect('panel_principal')