# Práctica 3 – Integración de patrones (Decorator, Observer, Template Method)

## 1. Objetivo
Ampliar el sistema de gestión de eventos implementado en Django incorporando tres patrones adicionales y conectándolos con los patrones ya existentes de prácticas anteriores.

## 2. Patrones implementados

### 2.1 Decorator (estructural)
**Ubicación:** `eventos/patrones/estructurales/decorator.py`

Se utiliza para añadir funcionalidades opcionales (extras) a un evento sin modificar su clase base.

- `EventoBase`: componente concreto con coste y descripción base.
- `EventoDecorator`: decorador abstracto.
- Decoradores concretos:
  - `MusicaEnVivoDecorator`
  - `CateringPremiumDecorator`
  - `SeguridadVIPDecorator`
  - `StreamingAvanzadoDecorator`

**Uso en la app:**
En `crear_evento_builder`, se aplican extras según parámetros de URL (`musica=1`, `catering=1`, `vip=1`, `streaming=1`) y se muestra resumen en el dashboard.

---

### 2.2 Observer (comportamiento)
**Ubicación:** `eventos/patrones/comportamiento/observer.py`

Permite notificar automáticamente a distintos subsistemas cuando un evento cambia de estado o fecha.

- `EventoObservable`: sujeto observable.
- `Observador`: interfaz.
- Observadores concretos:
  - `NotificadorEmail`
  - `NotificadorProveedor`
  - `NotificadorAnalytics`

**Uso en la app:**
Tras crear un evento, se registra un conjunto de observadores y se dispara `cambiar_estado("confirmado")`.  
Las notificaciones resultantes se guardan en sesión y se muestran en el dashboard.

---

### 2.3 Template Method (comportamiento)
**Ubicación:** `eventos/patrones/comportamiento/template_method.py`

Define un algoritmo estándar para el proceso de creación de eventos:

1. Validar datos  
2. Configurar servicios  
3. Calcular costes  
4. Confirmar evento

Subclases:
- `ProcesoConferencia`
- `ProcesoBoda`
- `ProcesoConcierto`

Cada subclase redefine los pasos específicos sin romper la estructura general.

**Uso en la app:**
En `crear_evento_builder`, se ejecuta el proceso correspondiente según tipo de evento y se guarda el log para visualizarlo en el dashboard.

---

## 3. Relación con patrones previos

- **Builder**: construye el evento base según tipo.
- **Prototype**: permite clonar eventos.
- **Singleton**: gestiona configuración global (moneda/impuestos).
- **Chain of Responsibility**: valida evento antes de guardarlo.
- **Bridge**: permite exportación HTML o JSON.
- **Adapter** y **Composite**: siguen integrados en la construcción y composición de servicios.

La práctica 3 se integra de forma incremental, manteniendo compatibilidad con la arquitectura existente.

---

## 4. Integración en interfaz web

Archivo principal de UI: `eventos/templates/eventos/dashboard.html`

Se añadieron:
- Resumen de extras aplicados (Decorator)
- Notificaciones automáticas (Observer)
- Historial de ejecución del algoritmo de creación (Template Method)

Además, los botones de creación incluyen query params para simular combinaciones de extras.

---

## 5. Pruebas

Se incluyeron pruebas unitarias e integración:

- `tests/unit/test_decorator.py`
- `tests/unit/test_observer.py`
- `tests/unit/test_template_method.py`
- `tests/integration/test_builder_decorator.py`
- `tests/integration/test_observer_eventos_reales.py`

También se mantuvieron/ajustaron pruebas previas para asegurar compatibilidad.

---

## 6. Problemas encontrados y solución

1. **Imports rotos tras reorganización**  
   - Se corrigieron imports absolutos antiguos (`from patrones...`) por imports relativos o `eventos.patrones...`.

2. **Import circular (`entidades` ↔ `builder`)**  
   - Se evitó importar `builder` desde `creacionales/__init__.py`.
   - Se simplificó `eventos/patrones/__init__.py` para no forzar cargas globales.

3. **Error `no such table: django_session`**  
   - Se detectó configuración de BD en memoria (`:memory:`).
   - Se cambió a SQLite en archivo (`BASE_DIR / "db.sqlite3"`).
   - Se ejecutaron migraciones correctamente.

---

## 7. Conclusión

La aplicación queda preparada con una arquitectura más flexible y mantenible:
- Extensible para añadir nuevos extras (Decorator)
- Reactiva a cambios de estado (Observer)
- Estandarizada en procesos de creación (Template Method)

La integración conserva compatibilidad con los patrones previos y deja una base sólida para evoluciones futuras.