import copy

class EventoPrototype:
    def clonar(self):
        """
        Realiza una copia profunda del objeto. 
        Garantiza que las estructuras anidadas (como listas de servicios)
        tengan nuevas referencias en memoria.
        """
        nuevo_evento = copy.deepcopy(self)
        
        nuevo_evento.id = None 
        return nuevo_evento