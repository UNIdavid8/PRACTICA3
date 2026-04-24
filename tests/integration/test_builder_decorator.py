from eventos.patrones.estructurales.decorator import EventoBase, CateringPremiumDecorator


def test_builder_decorator_basico():
    # Sustituye EventoBase por tu objeto real generado por Builder cuando lo conectes
    evento = EventoBase("Evento Builder", 1200.0)
    evento = CateringPremiumDecorator(evento)
    assert evento.get_coste() == 2400.0