from eventos.patrones.estructurales.composite import ComponenteServicio, PaqueteServicios
from eventos.patrones.estructurales.adapter import APIExternaStreaming, ProveedorStreamingAdapter
from eventos.patrones.comportamiento.chain_of_responsibility import (
    ManejadorValidacion, ValidarFecha, ValidarCapacidad
)
from eventos.patrones.estructurales.bridge import (
    ImplementacionExportacion, ExportadorHTML, ExportadorAPIJSON, AbstraccionRepresentacion
)