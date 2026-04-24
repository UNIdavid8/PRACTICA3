from dataclasses import dataclass, field
from typing import List, Optional
from eventos.patrones.creacionales.prototype import EventoPrototype

@dataclass
class Usuario:
    id: int
    username: str
    email: str
    is_organizador: bool = True

@dataclass
class Ubicacion:
    nombre: str
    direccion: str
    capacidad: int

@dataclass
class Servicio:
    nombre: str
    descripcion: str
    precio: float


@dataclass
class Evento(EventoPrototype): 
    id: int
    nombre: str
    tipo: str  # 'conferencia', 'boda', 'concierto'
    fecha: str
    ubicacion: Optional[Ubicacion] = None
    servicios: List[Servicio] = field(default_factory=list)
    
    def agregar_servicio(self, servicio: Servicio):
        self.servicios.append(servicio)