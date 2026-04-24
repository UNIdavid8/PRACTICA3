

db_usuarios = {}
db_eventos = {}


secuencia_usuarios = 1
secuencia_eventos = 1

def guardar_evento(evento):
    global secuencia_eventos
    if not evento.id:
        evento.id = secuencia_eventos
        secuencia_eventos += 1
    db_eventos[evento.id] = evento
    return evento

def obtener_evento(evento_id):
    return db_eventos.get(evento_id)