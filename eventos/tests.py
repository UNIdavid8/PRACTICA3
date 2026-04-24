from django.test import SimpleTestCase
from .patrones.creacionales.singleton import ConfiguracionGlobal
from .patrones.creacionales.builder import DirectorEvento, EventoConferenciaBuilder
from .entidades import Ubicacion, Evento, Servicio

class PatronesDesignTests(SimpleTestCase):

    def test_singleton_instancia_unica(self):
        """Verifica que múltiples llamadas al Singleton devuelvan la misma referencia en memoria[cite: 109]."""
        config1 = ConfiguracionGlobal()
        config2 = ConfiguracionGlobal()
        

        self.assertIs(config1, config2)
        

        config1.actualizar_configuracion(moneda="JPY")
        self.assertEqual(config2.moneda, "JPY")

    def test_builder_ensamblaje_conferencia(self):
        """Verifica que el Builder construya el evento con los servicios correctos[cite: 62]."""
        director = DirectorEvento()
        builder = EventoConferenciaBuilder()
        director.builder = builder
        
        ubicacion = Ubicacion("Test Room", "Calle Falsa 123", 100)
        director.construir_conferencia_estandar("Conf Test", "2026-01-01", ubicacion)
        
        evento = builder.get_resultado()
        
        self.assertEqual(evento.nombre, "Conf Test")
        self.assertEqual(evento.tipo, "Conferencia")

        nombres_servicios = [s.nombre for s in evento.servicios]
        self.assertIn("Streaming 4K", nombres_servicios)

    def test_prototype_clonacion_profunda(self):
        """Verifica que el Prototype realice una copia profunda sin referenciar al original[cite: 110]."""
        evento_original = Evento(id=1, nombre="Original", tipo="Boda", fecha="2026-01-01")
        servicio_test = Servicio("DJ", "Música", 500)
        evento_original.agregar_servicio(servicio_test)
        
        evento_clonado = evento_original.clonar()
        evento_clonado.nombre = "Clon"
        

        self.assertIsNot(evento_original, evento_clonado)
        self.assertNotEqual(evento_original.nombre, evento_clonado.nombre)
        

        self.assertIsNot(evento_original.servicios, evento_clonado.servicios)
        

        evento_clonado.agregar_servicio(Servicio("Barra Libre", "Bebidas", 1000))
        self.assertEqual(len(evento_original.servicios), 1)
        self.assertEqual(len(evento_clonado.servicios), 2)