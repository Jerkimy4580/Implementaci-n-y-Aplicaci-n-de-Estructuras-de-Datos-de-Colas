# Tarea: Listas enlazadas, pilas y colas (Parte 3)

**Estudiante:** Jeremy Arévalo  
**Lenguaje:** Python 3.10 o superior  
**Tema 6.5:** Colas y operaciones básicas (`enqueue`, `dequeue`, `front`).  
**Tema 6.6:** Colas circulares y colas de prioridad.

## 1. Introducción

Una **cola** es una estructura de datos que normalmente sigue el principio **FIFO (First In, First Out)**: el primer elemento que entra es el primero que sale. Las colas circulares reutilizan posiciones de memoria y las colas de prioridad seleccionan elementos según una regla de importancia. En una cola de prioridad, cuando varios elementos comparten prioridad, se puede preservar su orden de llegada.

Este proyecto contiene cuatro programas independientes que explican y demuestran el uso de cada estructura mediante ejemplos de atención, planificación de procesos y servicios bancarios.

## 2. Archivos del proyecto

```text
tarea_colas_parte3/
├── problema1.py              # Cola básica con lista enlazada
├── problema2.py              # Cola circular y Round Robin
├── problema3.py              # Cola de prioridad hospitalaria
├── problema4.py              # Banco: cola simple y de prioridad
├── requirements.txt          # Dependencias
├── README.md                 # Documentación y comparación
├── tests/
│   └── test_queues.py       # Pruebas automáticas
└── evidencias/
    └── LEEME.md             # Organización de evidencias
```

**Independencia:** cada archivo `.py` contiene sus clases y una demostración propia. Al ejecutar cada archivo se inicia automáticamente su ejemplo, sin depender de un programa principal compartido.

## 3. Requisitos y ejecución

- Python **3.10 o superior**.
- Biblioteca estándar de Python (`dataclasses`, `collections`, `heapq`, `unittest`).
- No hay dependencias externas.


Para ejecutar cada problema por separado:

```bash
python problema1.py
python problema2.py
python problema3.py
python problema4.py
```

En Windows también se puede ejecutar con `py problema1.py`. En algunos sistemas Linux o macOS el comando equivalente es `python3 problema1.py`.

Los datos de demostración están definidos en la función `run_demo()` de cada archivo. Los métodos de las clases permiten trabajar con otros datos y se validan en las pruebas automáticas.

---

## 4. Problema 1: Implementación de cola básica

**Archivo:** `problema1.py`  
**Estructura:** Lista enlazada simple con cola FIFO.  
**Clase:** `Cola`.

### Enfoque y decisiones de diseño

La cola se implementa con nodos `Node`. Cada nodo almacena un elemento y una referencia al siguiente nodo. La clase `Cola` conserva dos referencias: una al **frente** (`_first`) y otra al **final** (`_last`). De este modo, tanto insertar como retirar elementos se puede realizar sin recorrer toda la lista.

La implementación ofrece los cinco métodos solicitados:

| Método | Funcionamiento |
| --- | --- |
| `enqueue(element)` | Crea un nodo y lo añade al final. |
| `dequeue()` | Elimina y devuelve el primer nodo. |
| `front()` | Devuelve el primer elemento sin eliminarlo. |
| `is_empty()` | Retorna `True` si no quedan nodos. |
| `size()` | Devuelve el número de elementos almacenados. |

Cuando se elimina el último nodo, se limpian las referencias al frente y al final. Esto permite reutilizar la cola correctamente. Se utiliza `IndexError` para controlar consultas o extracciones de una cola vacía.

### Ejemplo de entrada y salida

**Entrada:** se registran, por orden, `Ana`, `Luis` y `Marta`.

**Salida principal:**

```text
¿Está vacía al inicio?: True
enqueue(Ana) -> ['Ana']
enqueue(Luis) -> ['Ana', 'Luis']
enqueue(Marta) -> ['Ana', 'Luis', 'Marta']
front(): Ana
size(): 3
dequeue(): Ana
front() después de retirar: Luis
dequeue(): Luis
dequeue(): Marta
¿Está vacía al terminar?: True
Error controlado: No se puede retirar: la cola está vacía.
Reutilización de la cola: ['Sofía']
```

**Interpretación del resultado:** las personas salen en el mismo orden de llegada, lo que confirma el funcionamiento FIFO. También se demuestra que la cola puede vaciarse y utilizarse nuevamente.

### Complejidad

- `enqueue`, `dequeue`, `front`, `is_empty` y `size`: **O(1)**.
- `show_queue`: **O(n)**, porque recorre los nodos para preparar la lista visible.
- Espacio total: **O(n)** para almacenar `n` elementos.

---

## 5. Problema 2: Cola circular para gestión de procesos

**Archivo:** `problema2.py`  
**Estructura:** Arreglo circular de capacidad fija.  
**Clase:** `ColaCircular`.

### Enfoque y decisiones de diseño

La cola circular utiliza un arreglo y dos índices: `_front_index` y `_rear_index`. Los índices avanzan con la operación **módulo** (`%`), por lo que al llegar al final del arreglo regresan al inicio. Así se reutilizan los espacios liberados sin desplazar todos los elementos.

La clase implementa `enqueue`, `dequeue`, `front`, `is_empty` y `size`, además de `add_process`, `show_pending` y `run_round_robin`.

El algoritmo **Round Robin** entrega como máximo **3 unidades de tiempo (quantum)** a cada proceso:

1. Se extrae el proceso del frente.
2. Se ejecuta durante `min(3, tiempo restante)` unidades.
3. Si terminó, abandona la cola.
4. Si aún necesita CPU, vuelve al final de la cola.
5. Se muestran los procesos restantes después de cada turno.

La capacidad fija permite detectar el intento de añadir un sexto proceso cuando ya hay cinco posiciones ocupadas. Esta situación genera un error controlado `OverflowError`.

### Ejemplo de entrada

| Proceso | Tiempo requerido |
| --- | ---: |
| P1 | 7 |
| P2 | 4 |
| P3 | 9 |
| P4 | 2 |
| P5 | 5 |

**Quantum:** 3 unidades.

### Ejemplo de salida

```text
Quantum: 3
Cola inicial: P1(7) -> P2(4) -> P3(9) -> P4(2) -> P5(5)
Procesos registrados: 5
Primer proceso: P1
Error controlado: La cola circular está llena.
Turno 1: P1 ejecutó 3 unidades.
Procesos restantes: P2(4) -> P3(9) -> P4(2) -> P5(5) -> P1(4)
Turno 2: P2 ejecutó 3 unidades.
Procesos restantes: P3(9) -> P4(2) -> P5(5) -> P1(4) -> P2(1)
Turno 3: P3 ejecutó 3 unidades.
Procesos restantes: P4(2) -> P5(5) -> P1(4) -> P2(1) -> P3(6)
...
Turno 11: P3 ejecutó 3 unidades.
Proceso terminado: P3
Procesos restantes: Ninguno
Resumen: 11 turnos y 27 unidades ejecutadas.
Cola vacía al finalizar: True
Nuevo proceso después de finalizar: P6
```

**Interpretación del resultado:** los cinco procesos reciben CPU de forma alternada. El proceso P4 termina en su primer turno porque requiere solo 2 unidades; los demás regresan a la cola cuando no terminan. La suma de tiempos es **27 unidades** y se necesitan **11 turnos** para atenderlos a todos. Al finalizar, la cola puede reutilizarse.

### Complejidad

Sean **n** el número de procesos y **k** el número total de turnos Round Robin.

- `enqueue`, `dequeue`, `front`, `is_empty` y `size`: **O(1)** por operación.
- `show_pending`: **O(n)** por recorrido de los procesos activos.
- Simulación sin imprimir la cola en cada turno: **O(k)**.
- Simulación **con reporte de todos los procesos después de cada turno**, como se solicita: **O(k · n)** en el peor caso.
- Espacio: **O(c)** para una cola con capacidad fija `c`; en esta simulación `c = 5`.

Para tiempos iniciales `t₁, t₂, ..., tₙ` y quantum `q = 3`, el número de turnos es `k = Σ⌈tᵢ/q⌉`.

---

## 6. Problema 3: Cola de prioridad para emergencias

**Archivo:** `problema3.py`  
**Estructura:** Montículo mínimo (`heapq`).  
**Clase:** `ColaEmergencias`.

### Enfoque y decisiones de diseño

Cada paciente posee un nombre y una urgencia entre **1 y 5**, donde **1 es la más alta**. En vez de atender estrictamente por llegada, la cola de prioridad selecciona al paciente con el menor nivel numérico.

Para respetar el orden de llegada cuando coinciden las urgencias, cada elemento se guarda como una tupla:

```python
(urgency, arrival_order, patient)
```

La estructura `heapq` permite insertar y extraer pacientes sin ordenar toda la lista en cada operación. `arrival_order` garantiza que los pacientes con la misma urgencia se atiendan en orden FIFO. La función `show_waiting()` devuelve una lista ordenada para visualizar la espera sin alterar la cola original.

### Ejemplo de entrada

| Orden de llegada | Paciente | Urgencia |
| ---: | --- | ---: |
| 1 | Ana | 4 |
| 2 | Luis | 2 |
| 3 | Marta | 1 |
| 4 | Pedro | 3 |
| 5 | Sofía | 2 |
| 6 | Diego | 5 |
| 7 | Elena | 1 |
| 8 | Carlos | 3 |

### Ejemplo de salida

```text
Pacientes registrados: 8
Siguiente paciente: Marta
Orden de atención:
Atendido: Marta (urgencia 1)
Atendido: Elena (urgencia 1)
Atendido: Luis (urgencia 2)
Atendido: Sofía (urgencia 2)
Atendido: Pedro (urgencia 3)
Atendido: Carlos (urgencia 3)
Atendido: Ana (urgencia 4)
Atendido: Diego (urgencia 5)
Error controlado: No existen pacientes en espera.
Validación de urgencia: La urgencia debe ser un número entero entre 1 y 5.
```

**Interpretación del resultado:** Marta y Elena se atienden antes que los demás porque tienen urgencia 1; entre ellas se respeta el orden de llegada. Lo mismo ocurre con Luis y Sofía, ambos de urgencia 2. Esto confirma simultáneamente la priorización y el desempate FIFO.

### Complejidad

Sean **n** los pacientes en espera.

- `add_patient` (`enqueue` con prioridad): **O(log n)**.
- `attend_next` (`dequeue`): **O(log n)**.
- `front`, `size` e `is_empty`: **O(1)**.
- `show_waiting`: **O(n log n)** para obtener la vista ordenada.
- Espacio: **O(n)** para la cola de pacientes.

---

## 7. Problema 4: Sistema de atención al cliente en un banco (opción C)

**Archivo:** `problema4.py`  
**Estructuras:** Cola simple FIFO (`deque`) y cola de prioridad (`heapq`).  
**Clases principales:** `SimpleQueue`, `PriorityQueue`, `ServiceQueue` y `BankSystem`.

### Enfoque y funcionamiento detallado

El banco atiende tres servicios independientes:

- **Caja**: operaciones de caja.
- **Préstamos**: trámites de crédito.
- **Consultas**: información y atención general.

Cada servicio dispone de **dos colas**:

1. **Cola simple:** almacena a los clientes normales con `deque`, conservando el orden de llegada.
2. **Cola de prioridad:** almacena a los adultos mayores y clientes premium usando `heapq`.

La política elegida es **Adulto mayor > Premium > Normal**. Los clientes de una misma categoría prioritaria se atienden por orden de llegada. Una vez que termina la cola prioritaria del servicio, se atiende a los clientes normales en orden FIFO.

El sistema no mezcla a los usuarios de Caja con los de Préstamos o Consultas. De esta forma, cada área puede atender su propia lista, evitando bloquear a un cliente por un trámite de otro tipo. Es un modelo de **selección de turnos**, no una simulación de tiempos reales de atención.

### Ejemplo de entrada

| Cliente | Servicio | Categoría |
| --- | --- | --- |
| Ana | Caja | Normal |
| Luis | Préstamos | Premium |
| Marta | Caja | Adulto mayor |
| Pedro | Consultas | Normal |
| Sofía | Caja | Premium |
| Diego | Préstamos | Normal |
| Elena | Caja | Normal |
| Carlos | Consultas | Adulto mayor |
| Valeria | Préstamos | Adulto mayor |
| Julia | Caja | Premium |

### Ejemplo de salida

```text
Servicio: Caja
Espera prioritaria: ['Marta (Adulto mayor)', 'Sofía (Premium)', 'Julia (Premium)']
Espera normal: ['Ana', 'Elena']
Orden de atención:
- Marta (Adulto mayor)
- Sofía (Premium)
- Julia (Premium)
- Ana (Normal)
- Elena (Normal)

Servicio: Préstamos
Espera prioritaria: ['Valeria (Adulto mayor)', 'Luis (Premium)']
Espera normal: ['Diego']
Orden de atención:
- Valeria (Adulto mayor)
- Luis (Premium)
- Diego (Normal)

Servicio: Consultas
Espera prioritaria: ['Carlos (Adulto mayor)']
Espera normal: ['Pedro']
Orden de atención:
- Carlos (Adulto mayor)
- Pedro (Normal)

Error controlado: No hay clientes esperando en Caja.
Validación de servicio: Servicio inválido. Use Caja, Préstamos o Consultas.
```

**Interpretación del resultado:** en Caja, Marta se atiende primero por ser adulta mayor, después Sofía y Julia por ser premium, y al final Ana y Elena por orden de llegada. Los servicios de Préstamos y Consultas mantienen sus propias listas. El resultado demuestra el uso combinado de **FIFO y prioridad**.

### Complejidad

Sean **p** los clientes prioritarios y **r** los normales de un servicio.

- Registrar un cliente normal: **O(1)** amortizado.
- Registrar un cliente prioritario: **O(log p)**.
- Atender un cliente normal: **O(1)**.
- Atender un cliente prioritario: **O(log p)**.
- Consultar si quedan clientes: **O(1)**.
- Mostrar la lista de espera: **O(p log p + r)**.
- Espacio total: **O(p + r)** para las colas de un servicio, u **O(n)** para todos los clientes del banco.

**Limitación:** con prioridad estricta, una llegada continua de clientes prioritarios puede aumentar la espera de clientes normales. El ejercicio garantiza las prioridades solicitadas, pero no implementa una política adicional contra la espera indefinida.

---

## 8. Análisis comparativo de los tipos de colas

### 8.1 Complejidad temporal de las operaciones básicas

| Operación | Cola simple enlazada | Cola circular (arreglo) | Cola de prioridad (heap) |
| --- | --- | --- | --- |
| `enqueue` | **O(1)** | **O(1)** | **O(log n)** |
| `dequeue` | **O(1)** | **O(1)** | **O(log n)** |
| `front` | **O(1)** | **O(1)** | **O(1)** |
| `is_empty` | **O(1)** | **O(1)** | **O(1)** |
| `size` | **O(1)** | **O(1)** | **O(1)** |
| Mostrar todos en orden | O(n) | O(n) | O(n log n) |
| Memoria para n elementos | O(n) | O(c), capacidad fija c | O(n) |

**Nota:** para las listas Python usadas como montículo, las operaciones `heapq.heappush()` y `heapq.heappop()` tienen complejidad O(log n). En la cola enlazada se mantienen referencias al primero y al último nodo. En la cola circular se utilizan índices y no se desplazan elementos.

### 8.2 Ventajas y desventajas

| Tipo | Ventajas | Desventajas |
| --- | --- | --- |
| **Cola simple** | Fácil de implementar y entender; FIFO justo por llegada; inserción y extracción O(1). | No distingue prioridades; la lista enlazada utiliza referencias adicionales por nodo. |
| **Cola circular** | Reutiliza espacios de un arreglo; operaciones O(1); adecuada para turnos repetitivos. | La implementación tiene una capacidad máxima; si se llena, no admite nuevos procesos hasta liberar espacio. |
| **Cola de prioridad** | Atiende primero los casos importantes; inserciones y extracciones eficientes con heap; permite desempates por llegada. | No sigue FIFO global; es más compleja y los elementos de prioridad baja pueden esperar mucho. |

### 8.3 Escenarios de uso óptimos

| Tipo de cola | Escenarios recomendados | Motivo |
| --- | --- | --- |
| **Simple** | Filas de atención general, tickets, mensajes de tareas | Mantiene el orden de llegada con costo constante. |
| **Circular** | Planificador Round Robin, buffers, procesamiento periódico | Reutiliza posiciones y rota los turnos eficientemente. |
| **Prioridad** | Hospitales, incidentes críticos, servicios preferenciales | Selecciona primero los elementos con mayor importancia. |

### 8.4 Justificación de las estructuras de Python utilizadas

- **Nodos enlazados (Problema 1):** muestran directamente cómo funciona una lista enlazada sin depender de una colección que oculte los punteros.
- **Arreglo circular (Problema 2):** hace visibles los índices circulares y permite comprobar la reutilización de memoria.
- **Montículo `heapq` (Problema 3):** mantiene eficiente la selección del paciente de mayor urgencia y el orden de llegada en empates.
- **`deque` y `heapq` (Problema 4):** combinan la eficiencia de una cola FIFO con la atención preferencial; cada servicio mantiene sus datos separados.

---

## 9. Buenas prácticas de programación

1. **Responsabilidad única:** cada método realiza una operación concreta; las demostraciones se mantienen en `run_demo()`.
2. **Nombres descriptivos en inglés:** por ejemplo, `remaining_time`, `add_patient`, `arrival_order`, `priority_queue` y `waiting_list`.
3. **Clases con los nombres solicitados:** `Cola`, `ColaCircular` y `ColaEmergencias`.
4. **Comentarios y docstrings en español:** explican reglas de negocio, estructuras y validaciones.
5. **Validaciones y manejo de errores:** colas vacías, colas llenas, urgencias fuera de rango, tiempos inválidos y servicios inexistentes.
6. **Independencia:** los cuatro archivos se ejecutan sin importar código de otro problema.
7. **Pruebas automáticas:** se verifica el orden FIFO, índices circulares, quantum, prioridades empatadas, validaciones y separación de servicios.

## 10. Pruebas automáticas

Se utiliza `unittest`, incluida en Python. Desde la carpeta del proyecto:

```bash
python -m unittest discover -s tests -v
```

Las **9 pruebas** comprueban:

- Los métodos básicos de `Cola`, la extracción en FIFO y la reutilización después de vaciarla.
- El comportamiento circular de los índices, la capacidad máxima y la validación de procesos.
- La simulación Round Robin con quantum 3, 11 turnos y 27 unidades ejecutadas.
- Los niveles de urgencia y los empates resueltos por orden de llegada.
- La atención preferencial, el orden FIFO normal, la separación entre servicios bancarios y los errores de entrada.

**Resultado de verificación:** 9 pruebas correctas.

## 11. Evidencias de ejecución

Las evidencias se organizan por problema en el directorio `evidencias/`.

| Problema | Captura correspondiente | Resultado que se verifica |
| --- | --- | --- |
| 1. Cola básica | `evidencias/problema1.png` | Orden FIFO, consultas, eliminación y cola vacía. |
| 2. Cola circular | `evidencias/problema2.png` | Cinco procesos, quantum 3 y cola después de cada turno. |
| 3. Emergencias | `evidencias/problema3.png` | Ocho pacientes, prioridad y empates por llegada. |
| 4. Banco | `evidencias/problema4.1.png` y `evidencias/problema4.2.png` | Atención por servicio, preferencias y FIFO normal. |

## 12. Conclusión

Los cuatro programas demuestran que cada tipo de cola resulta adecuado para necesidades distintas. La cola simple conserva el orden de llegada; la circular distribuye turnos y reutiliza posiciones; la de prioridad selecciona los elementos más importantes; y la solución bancaria combina dos estructuras para atender diferentes servicios y categorías. La comparación de complejidades confirma por qué cada implementación fue elegida para su problema.
