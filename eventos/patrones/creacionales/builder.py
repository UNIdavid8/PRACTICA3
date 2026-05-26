from abc import ABC, abstractmethod
from eventos.models import Evento
from .factory import ServicioFactory
from ..estructurales.composite import PaqueteServicios
from ..estructurales.adapter import ProveedorStreamingAdapter

class EventoBuilder(ABC):
    @abstractmethod
    def reset(self): pass
    @abstractmethod
    def set_datos_basicos(self, nombre, fecha): pass
    @abstractmethod
    def set_ubicacion(self, ubicacion): pass
    @abstractmethod
    def get_resultado(self): pass

class EventoConferenciaBuilder(EventoBuilder):
    def __init__(self): self.reset()
    def reset(self): self._evento = Evento(nombre="", tipo="Conferencia", fecha="")
    def set_datos_basicos(self, nombre, fecha):
        self._evento.nombre = nombre
        self._evento.fecha = fecha
    def set_ubicacion(self, ubicacion):
        self._evento.ubicacion = ubicacion
    def set_catering(self, tipo="estandar"):
        coste = 45.0 if tipo == "premium" else 15.0
        nombre = "Buffet de Gala" if tipo == "premium" else "Coffee Break"
        self._evento.agregar_servicio(ServicioFactory.crear(nombre, "Catering", coste))
    def set_streaming(self):
        adapter = ProveedorStreamingAdapter("4K")
        self._evento.agregar_servicio(adapter.obtener_servicio())
    def get_resultado(self):
        res = self._evento
        self.reset()
        return res

class EventoBodaBuilder(EventoBuilder):
    def __init__(self): self.reset()
    def reset(self): self._evento = Evento(nombre="", tipo="Boda", fecha="")
    def set_datos_basicos(self, nombre, fecha):
        self._evento.nombre = nombre
        self._evento.fecha = fecha
    def set_ubicacion(self, ubicacion):
        self._evento.ubicacion = ubicacion
    def set_catering(self):
        self._evento.agregar_servicio(ServicioFactory.crear("Banquete Nupcial", "Menú degustación", 120.0))
    def set_decoracion(self, estilo="clasico"):
        precio = 300.0 if estilo == "clasico" else 600.0
        self._evento.agregar_servicio(ServicioFactory.crear(f"Decoración {estilo}", "Ambientación", precio))
    def get_resultado(self):
        res = self._evento
        self.reset()
        return res

class EventoConciertoBuilder(EventoBuilder):
    def __init__(self): self.reset()
    def reset(self): self._evento = Evento(nombre="", tipo="Concierto", fecha="")
    def set_datos_basicos(self, nombre, fecha):
        self._evento.nombre = nombre
        self._evento.fecha = fecha
    def set_ubicacion(self, ubicacion):
        self._evento.ubicacion = ubicacion
    def set_catering(self):
        self._evento.agregar_servicio(ServicioFactory.crear("Backstage", "Comida", 300.0))
    def set_sonido(self, potencia="Line Array"):
        self._evento.agregar_servicio(ServicioFactory.crear(f"Sonido {potencia}", "Audio pro", 1500.0))
    def get_resultado(self):
        res = self._evento
        self.reset()
        return res

class EventoCenaEmpresaBuilder(EventoBuilder):
    def __init__(self): self.reset()
    def reset(self): self._evento = Evento(nombre="", tipo="Cena Empresa", fecha="")
    def set_datos_basicos(self, nombre, fecha):
        self._evento.nombre = nombre
        self._evento.fecha = fecha
    def set_ubicacion(self, ubicacion):
        self._evento.ubicacion = ubicacion
    def set_catering(self, menu="Ejecutivo"):
        self._evento.agregar_servicio(ServicioFactory.crear(f"Menú {menu}", "Cena", 80.0))
    def set_entretenimiento(self):
        pack = PaqueteServicios("Fin de Fiesta")
        pack.agregar(ServicioFactory.crear("Monologuista", "Show 1h", 400.0))
        pack.agregar(ServicioFactory.crear("Barra Libre", "Premium", 900.0))
        self._evento.agregar_servicio(pack.obtener_servicio())
    def get_resultado(self):
        res = self._evento
        self.reset()
        return res

class DirectorEvento:
    def __init__(self): self._builder = None
    @property
    def builder(self): return self._builder
    @builder.setter
    def builder(self, builder): self._builder = builder
    def construir_conferencia_estandar(self, nombre, fecha, ubicacion):
        self.builder.set_datos_basicos(nombre, fecha)
        self.builder.set_ubicacion(ubicacion)
        self.builder.set_catering(tipo="estandar")
        self.builder.set_streaming()
    def construir_boda_clasica(self, nombre, fecha, ubicacion):
        self.builder.set_datos_basicos(nombre, fecha)
        self.builder.set_ubicacion(ubicacion)
        self.builder.set_catering()
        self.builder.set_decoracion(estilo="clasico")
    def construir_concierto_rock(self, nombre, fecha, ubicacion):
        self.builder.set_datos_basicos(nombre, fecha)
        self.builder.set_ubicacion(ubicacion)
        self.builder.set_sonido("Estadio")
        self.builder.set_catering()
    def construir_cena_navidad(self, nombre, fecha, ubicacion):
        self.builder.set_datos_basicos(nombre, fecha)
        self.builder.set_ubicacion(ubicacion)
        self.builder.set_catering(menu="Premium")
        self.builder.set_entretenimiento()