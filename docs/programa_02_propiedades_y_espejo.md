# Programa 02 — Propiedades de la cámara y efecto espejo

Lee las propiedades de la cámara (resolución, FPS) y muestra el video con efecto espejo horizontal.

```python
import cv2

cap = cv2.VideoCapture(0)

ancho = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
alto = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
fps = cap.get(cv2.CAP_PROP_FPS)

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

Lee el valor de una propiedad de la cámara o video.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `propId` | `int` | Identificador de la propiedad. Se usa una constante de OpenCV. |

**Retorna:** `float` con el valor de la propiedad.

```python
ancho = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
alto  = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
fps   = cap.get(cv2.CAP_PROP_FPS)
```

#### Propiedades más usadas

| Constante | Descripción |
|---|---|
| `cv2.CAP_PROP_FRAME_WIDTH` | Ancho del frame en píxeles |
| `cv2.CAP_PROP_FRAME_HEIGHT` | Alto del frame en píxeles |
| `cv2.CAP_PROP_FPS` | Frames por segundo |
| `cv2.CAP_PROP_FRAME_COUNT` | Total de frames (solo en archivos de video) |
| `cv2.CAP_PROP_POS_FRAMES` | Frame actual (solo en archivos de video) |
| `cv2.CAP_PROP_BRIGHTNESS` | Brillo (si la cámara lo soporta) |
| `cv2.CAP_PROP_CONTRAST` | Contraste (si la cámara lo soporta) |

> **Nota:** `cap.get()` siempre retorna `float`. Usar `int()` para obtener valores enteros
> al imprimirlos o usarlos como dimensiones.

---

### `cap.set(propId, value)`

Modifica el valor de una propiedad de la cámara.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `propId` | `int` | Identificador de la propiedad (mismas constantes que `cap.get`). |
| `value` | `float` | Nuevo valor a asignar. |

**Retorna:** `bool` — `True` si la propiedad se pudo cambiar, `False` si no.

```python
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
```

> **Importante:** no todas las cámaras aceptan todos los valores. La cámara puede
> ignorar el cambio o ajustarlo al valor más cercano que soporte.

---

### `cv2.flip(src, flipCode)`

Voltea una imagen horizontal, vertical o en ambos ejes.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `src` | `numpy.ndarray` | Imagen de entrada. |
| `flipCode` | `int` | Eje de volteo (ver tabla abajo). |

**Retorna:** `numpy.ndarray` — imagen volteada (no modifica la original).

| `flipCode` | Efecto |
|---|---|
| `1` | Horizontal (espejo — izquierda/derecha) |
| `0` | Vertical (arriba/abajo) |
| `-1` | Ambos ejes a la vez |

```python
espejo     = cv2.flip(frame,  1)   # efecto espejo
invertido  = cv2.flip(frame,  0)   # boca abajo
rotado_180 = cv2.flip(frame, -1)   # 180 grados
```

> **Por qué espejo en webcam:** las cámaras capturan la imagen sin voltear,
> pero los humanos estamos acostumbrados a vernos en el espejo. El flip horizontal
> hace que el movimiento se sienta natural al verse en pantalla.

---

## Diferencia con el Programa 01

| Aspecto | Programa 01 | Programa 02 |
|---|---|---|
| Propiedades de cámara | No las lee | Las lee e imprime |
| Imagen mostrada | Original | Volteada horizontalmente |
| Funciones nuevas | — | `cap.get()`, `cap.set()`, `cv2.flip()` |

---

## Conceptos clave

- `cap.get()` y `cap.set()` se llaman **antes** del loop, no dentro.
- Las propiedades retornan `float`, convertir a `int` cuando se necesiten como enteros.
- `cv2.flip()` no modifica el frame original, retorna uno nuevo.
- El efecto espejo (`flipCode=1`) es el más usado en aplicaciones de videollamada.
