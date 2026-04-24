from rest_framework import serializers, viewsets
from rest_framework.response import Response
from .memoria import db_eventos



class ServicioSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=100)
    descripcion = serializers.CharField()
    precio = serializers.FloatField()

class UbicacionSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=100)
    direccion = serializers.CharField()
    capacidad = serializers.IntegerField()

class EventoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nombre = serializers.CharField()
    tipo = serializers.CharField()
    fecha = serializers.CharField()
    ubicacion = UbicacionSerializer(allow_null=True)
    servicios = ServicioSerializer(many=True)



class EventoViewSet(viewsets.ViewSet):
    """
    Expone las operaciones de lectura de la base de datos en memoria.
    """
    def list(self, request):
        """GET /eventos/api/v1/eventos/"""
        eventos = list(db_eventos.values())
        serializer = EventoSerializer(eventos, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """GET /eventos/api/v1/eventos/{id}/"""
        evento = db_eventos.get(int(pk))
        if evento:
            serializer = EventoSerializer(evento)
            return Response(serializer.data)
        return Response({"error": "Evento no encontrado"}, status=404)