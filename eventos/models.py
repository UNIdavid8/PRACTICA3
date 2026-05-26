from django.db import models

class Ubicacion(models.Model):
    nombre = models.CharField(max_length=200)
    direccion = models.CharField(max_length=200)
    capacidad = models.IntegerField()

class Evento(models.Model):
    nombre = models.CharField(max_length=200)
    tipo = models.CharField(max_length=100)
    fecha = models.CharField(max_length=50)
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE, null=True)
    estado_actual = models.CharField(max_length=50, default="BORRADOR")
    coste_base = models.FloatField(default=1000.0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.servicios_temporales = []

    def agregar_servicio(self, servicio):
        self.servicios_temporales.append(servicio)

    def clonar(self):
        clon = Evento.objects.get(pk=self.pk)
        clon.pk = None
        clon.nombre = f"Copia de {self.nombre}"
        clon.estado_actual = "BORRADOR"
        clon.save()
        for servicio in self.servicios.all():
            servicio.pk = None
            servicio.evento = clon
            servicio.save()
        return clon

    def crear_observable(self):
        from .patrones.comportamiento.observer import EventoObservable
        return EventoObservable(self)

class Servicio(models.Model):
    evento = models.ForeignKey(Evento, related_name="servicios", on_delete=models.CASCADE, null=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=500)
    coste = models.FloatField()