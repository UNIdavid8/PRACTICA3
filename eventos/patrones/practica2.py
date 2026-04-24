from patrones.composite import ComponenteServicio, PaqueteServicios
from patrones.adapter import APIExternaStreaming, ProveedorStreamingAdapter
from patrones.chain_of_responsibility import (
    ManejadorValidacion,
    ValidarFecha,
    ValidarCapacidad,
)
from patrones.bridge import (
    ImplementacionExportacion,
    ExportadorHTML,
    ExportadorAPIJSON,
    AbstraccionRepresentacion,
)