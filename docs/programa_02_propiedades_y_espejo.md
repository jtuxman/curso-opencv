# Programa 02 — Propiedades de la cámara y efecto espejo

Lee las propiedades de la cámara (resolución, FPS) y muestra el video con efecto espejo horizontal.

```python
import cv2

cap = cv2.VideoCapture(0)

ancho = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
alto  = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
fps   = cap.get(cv2.CAP_PROP_FPS)

print(f"Resolución: {int(ancho)} x {int(alto)}")
print(f"FPS: {fps}")

while True:
    ret, frame = cap.read()

    if not ret:
        break

    frame_espejo = cv2.flip(frame, 1)

    cv2.imshow("Camara espejo", frame_espejo)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
```

---

## Funciones nuevas en este programa

### `cap.get(propId)`

Lee el valor actual de una propiedad del dispositivo de captura.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `propId` | `int` | Identificador de la propiedad. Se usa una constante de OpenCV (`cv2.CAP_PROP_...`). |

**Retorna:** `float` — siempre retorna `float` incluso para propiedades enteras.

**Ejemplos:**

```python
# Propiedades de dimensión y tiempo:
ancho   = cap.get(cv2.CAP_PROP_FRAME_WIDTH)    # → 640.0
alto    = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)   # → 480.0
fps     = cap.get(cv2.CAP_PROP_FPS)            # → 30.0

# Convertir a int cuando se necesite como número entero:
ancho_px = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))   # → 640

# Propiedades de imagen (si la cámara las soporta):
brillo   = cap.get(cv2.CAP_PROP_BRIGHTNESS)   # nivel de brillo
contraste = cap.get(cv2.CAP_PROP_CONTRAST)    # nivel de contraste
saturacion = cap.get(cv2.CAP_PROP_SATURATION) # saturación de color

# Propiedades de navegación (solo en archivos de video):
total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)  # total de frames del video
frame_actual = cap.get(cv2.CAP_PROP_POS_FRAMES)   # frame en el que estamos
posicion_ms  = cap.get(cv2.CAP_PROP_POS_MSEC)     # posición en milisegundos
```

#### Propiedades más usadas

| Constante | Descripción | Unidad |
|---|---|---|
| `cv2.CAP_PROP_FRAME_WIDTH` | Ancho del frame | Píxeles |
| `cv2.CAP_PROP_FRAME_HEIGHT` | Alto del frame | Píxeles |
| `cv2.CAP_PROP_FPS` | Frames por segundo | FPS |
| `cv2.CAP_PROP_FRAME_COUNT` | Total de frames (videos) | Frames |
| `cv2.CAP_PROP_POS_FRAMES` | Frame actual (videos) | Frames |
| `cv2.CAP_PROP_BRIGHTNESS` | Brillo | 0.0 – 1.0 |
| `cv2.CAP_PROP_CONTRAST` | Contraste | 0.0 – 1.0 |

---

### `cap.set(propId, value)`

Modifica el valor de una propiedad del dispositivo de captura.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `propId` | `int` | Identificador de la propiedad (mismas constantes que `cap.get`). |
| `value` | `float` | Nuevo valor a asignar. |

**Retorna:** `bool` — `True` si la propiedad se modificó, `False` si el dispositivo no la soporta.

**Ejemplos:**

```python
# Cambiar resolución (debe llamarse ANTES del loop):
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Verificar si el cambio fue aceptado:
exito = cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
if not exito:
    print("La cámara no soporta 1920px de ancho")

# La cámara puede aceptar el set() pero ajustar al valor soportado más cercano:
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 9999)  # pide 9999, pero la cámara pone 1920
ancho_real = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
print(f"Ancho real: {int(ancho_real)}")  # muestra el valor que realmente quedó

# Navegar a un frame específico en un video:
cap.set(cv2.CAP_PROP_POS_FRAMES, 100)   # ir al frame número 100
cap.set(cv2.CAP_PROP_POS_MSEC, 5000)   # ir al segundo 5 (5000 ms)
```

> **Importante:** `cap.set()` y `cap.get()` deben llamarse **antes del loop**
> porque son operaciones sobre la configuración del dispositivo, no del frame.
> Llamarlas dentro del loop en cada iteración es innecesario y lento.

---

### `cv2.flip(src, flipCode)`

Voltea una imagen horizontal, vertical o en ambos ejes.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `src` | `numpy.ndarray` | Imagen de entrada (cualquier número de canales). |
| `flipCode` | `int` | Eje de volteo: `1` = horizontal, `0` = vertical, `-1` = ambos. |

**Retorna:** `numpy.ndarray` — imagen volteada. **No modifica la imagen original.**

**Ejemplos:**

```python
# Efecto espejo (más natural para verse en cámara):
espejo = cv2.flip(frame, 1)
# Antes: [A B C D]   Después: [D C B A]
#        [E F G H]            [H G F E]

# Volteo vertical (boca abajo):
invertido = cv2.flip(frame, 0)
# Antes: [A B C D]   Después: [I J K L]   ← última fila primero
#        [E F G H]            [E F G H]
#        [I J K L]            [A B C D]   ← primera fila al final

# Rotación 180° (equivale a voltear en ambos ejes):
rotado_180 = cv2.flip(frame, -1)

# Aplicar flip en una región específica (recorte + flip + reemplazar):
region = frame[100:300, 200:400]       # recortar región
region_espejo = cv2.flip(region, 1)    # voltear solo esa región
frame[100:300, 200:400] = region_espejo  # reemplazar en el frame original

# flip no modifica el original, se puede comparar:
original = frame.copy()
espejo   = cv2.flip(frame, 1)
cv2.imshow("Original", original)
cv2.imshow("Espejo",   espejo)
```

> **¿Por qué el efecto espejo?** Las cámaras capturan la imagen sin voltear,
> pero los humanos estamos acostumbrados a vernos en el espejo. Sin el flip,
> levantar la mano derecha aparece como si levantaras la izquierda en pantalla,
> lo que resulta desorientador en videollamadas o filtros de cámara.

---

## Diferencia con el Programa 01

| Aspecto | Programa 01 | Programa 02 |
|---|---|---|
| Propiedades de cámara | No las lee | Lee e imprime resolución y FPS |
| Imagen mostrada | Original | Volteada horizontalmente |
| Funciones nuevas | — | `cap.get()`, `cap.set()`, `cv2.flip()` |

---

## Conceptos clave

- `cap.get()` siempre retorna `float`; usar `int()` para valores de píxeles.
- `cap.get()` y `cap.set()` se llaman **antes** del loop, no dentro.
- `cv2.flip()` retorna una copia — no modifica el frame original.
- El efecto espejo (`flipCode=1`) hace los movimientos más naturales frente a cámara.
