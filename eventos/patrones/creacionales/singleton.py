class ConfiguracionGlobal:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(ConfiguracionGlobal, cls).__new__(cls)
            cls._instancia.moneda = "EUR"
            cls._instancia.impuestos = 21.0
            cls._instancia.limite_asistentes = 5000
        return cls._instancia

    def actualizar_configuracion(self, **kwargs):
        for clave, valor in kwargs.items():
            if hasattr(self, clave):
                setattr(self, clave, valor)