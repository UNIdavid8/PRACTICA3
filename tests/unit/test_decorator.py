from eventos.patrones.estructurales.decorator import (
    EventoBase,
    MusicaEnVivoDecorator,
    CateringPremiumDecorator,
    SeguridadVIPDecorator,
)


def test_evento_base_sin_extras():
    evento = EventoBase("Tech Day", 1000.0)
    assert evento.get_coste() == 1000.0
    assert "Tech Day" in evento.get_descripcion()


def test_evento_con_multiples_decoradores():
    evento = EventoBase("Tech Day", 1000.0)
    evento = MusicaEnVivoDecorator(evento)
    evento = CateringPremiumDecorator(evento)
    evento = SeguridadVIPDecorator(evento)

    assert evento.get_coste() == 1000.0 + 500.0 + 1200.0 + 800.0
    descripcion = evento.get_descripcion()
    assert "Música en vivo" in descripcion
    assert "Catering premium" in descripcion
    assert "Seguridad VIP" in descripcion