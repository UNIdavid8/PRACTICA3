from abc import ABC, abstractmethod
from eventos.entidades import Evento, Servicio, Ubicacion
from .practica2 import PaqueteServicios, ProveedorStreamingAdapter # NUEVAS IMPORTACIONES

class EventoBuilder(ABC):
    @abstractmethod
    def reset(self): pass
    @abstractmethod
    def set_datos_basicos(self, nombre: str, fecha: str): pass
    @abstractmethod
    def set_ubicacion(self, ubicacion: Ubicacion): pass
    @abstractmethod
    def get_resultado(self) -> Evento: pass

class EventoConferenciaBuilder(EventoBuilder):
    def __init__(self): self.reset()
    def reset(self): self._evento = Evento(id=None, nombre="", tipo="Conferencia", fecha="")
    
    def set_datos_basicos(self, nombre: str, fecha: str):
        self._evento.nombre = nombre
        self._evento.fecha = fecha

    def set_ubicacion(self, ubicacion: Ubicacion):
        self._evento.ubicacion = ubicacion

    def set_catering(self, tipo="estandar"):
        if tipo == "premium":
            self._evento.agregar_servicio(Servicio("Buffet de Gala", "Cena completa", 45.0))
        else:
            self._evento.agregar_servicio(Servicio("Coffee Break", "Café y pastas", 15.0))

    def set_streaming(self):
        # INTEGRACIÓN ADAPTER: Inyectamos el servicio externo adaptado
        adapter = ProveedorStreamingAdapter("4K")
        self._evento.agregar_servicio(adapter.obtener_servicio())

    def get_resultado(self) -> Evento:
        res = self._evento
        self.reset()
        return res

class EventoBodaBuilder(EventoBuilder):
    def __init__(self): self.reset()
    def reset(self): self._evento = Evento(id=None, nombre="", tipo="Boda", fecha="")
    
    def set_datos_basicos(self, nombre: str, fecha: str):
        self._evento.nombre = nombre
        self._evento.fecha = fecha

    def set_ubicacion(self, ubicacion: Ubicacion):
        self._evento.ubicacion = ubicacion

    def set_catering(self):
        self._evento.agregar_servicio(Servicio("Banquete Nupcial", "Menú degustación", 120.0))

    def set_decoracion(self, estilo="clasico"):
        precio = 300.0 if estilo == "clasico" else 600.0
        self._evento.agregar_servicio(Servicio(f"Decoración {estilo.capitalize()}", "Ambientación", precio))

    def get_resultado(self) -> Evento:
        res = self._evento
        self.reset()
        return res

class EventoConciertoBuilder(EventoBuilder):
    def __init__(self): self.reset()
    def reset(self): self._evento = Evento(id=None, nombre="", tipo="Concierto", fecha="")
    
    def set_datos_basicos(self, nombre: str, fecha: str):
        self._evento.nombre = nombre
        self._evento.fecha = fecha
        
    def set_ubicacion(self, ubicacion: Ubicacion): 
        self._evento.ubicacion = ubicacion
        
    def set_catering(self): 
        self._evento.agregar_servicio(Servicio("Backstage Catering", "Comida artistas", 300.0))
        
    def set_sonido(self, potencia="Line Array"):
        self._evento.agregar_servicio(Servicio(f"Equipo de Sonido {potencia}", "Audio pro", 1500.0))
        
    def get_resultado(self) -> Evento:
        res = self._evento
        self.reset()
        return res

class EventoCenaEmpresaBuilder(EventoBuilder):
    def __init__(self): self.reset()
    def reset(self): self._evento = Evento(id=None, nombre="", tipo="Cena Empresa", fecha="")
    
    def set_datos_basicos(self, nombre: str, fecha: str):
        self._evento.nombre = nombre
        self._evento.fecha = fecha
        
    def set_ubicacion(self, ubicacion: Ubicacion): 
        self._evento.ubicacion = ubicacion
        
    def set_catering(self, menu="Ejecutivo"):
        self._evento.agregar_servicio(Servicio(f"Menú {menu}", "Cena de empresa", 80.0))
        
    def set_entretenimiento(self):
        # INTEGRACIÓN COMPOSITE: Creamos un paquete de servicios unificado
        pack = PaqueteServicios("Fin de Fiesta")
        pack.agregar(Servicio("Monologuista", "Show 1h", 400.0))
        pack.agregar(Servicio("Barra Libre", "Premium", 900.0))
        self._evento.agregar_servicio(pack.obtener_servicio())
        
    def get_resultado(self) -> Evento:
        res = self._evento
        self.reset()
        return res

class DirectorEvento:
    def __init__(self): self._builder = None
    @property
    def builder(self) -> EventoBuilder: return self._builder
    @builder.setter
    def builder(self, builder: EventoBuilder): self._builder = builder

    def construir_conferencia_estandar(self, nombre: str, fecha: str, ubicacion: Ubicacion):
        self.builder.set_datos_basicos(nombre, fecha)
        self.builder.set_ubicacion(ubicacion)
        self.builder.set_catering(tipo="estandar")
        self.builder.set_streaming()

    def construir_boda_clasica(self, nombre: str, fecha: str, ubicacion: Ubicacion):
        self.builder.set_datos_basicos(nombre, fecha)
        self.builder.set_ubicacion(ubicacion)
        self.builder.set_catering()
        self.builder.set_decoracion(estilo="clasico")

    def construir_concierto_rock(self, nombre: str, fecha: str, ubicacion: Ubicacion):
        self.builder.set_datos_basicos(nombre, fecha)
        self.builder.set_ubicacion(ubicacion)
        self.builder.set_sonido("Estadio")
        self.builder.set_catering()

    def construir_cena_navidad(self, nombre: str, fecha: str, ubicacion: Ubicacion):
        self.builder.set_datos_basicos(nombre, fecha)
        self.builder.set_ubicacion(ubicacion)
        self.builder.set_catering(menu="Premium")
        self.builder.set_entretenimiento()