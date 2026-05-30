# Programa 04 — Dibujar en el frame

Dibuja formas geométricas y texto directamente sobre el frame de la cámara en tiempo real.

```python
import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    alto, ancho = frame.shape[:2]

    cv2.rectangle(frame, (10, 10), (200, 60), (0, 255, 0), 2)

    centro = (ancho // 2, alto // 2)
    cv2.circle(frame, centro, 50, (255, 0, 0), 3)

    cv2.line(frame, (0, 0), (ancho, alto), (0, 0, 255), 1)

    cv2.putText(frame, "Presiona Q para salir", (10, alto - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    cv2.imshow("Dibujo en frame", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
```

---

## Concepto previo: coordenadas y `frame.shape`

Antes de dibujar es necesario entender el sistema de coordenadas de OpenCV.

### Sistema de coordenadas

```
(0,0) ──────────────► X (ancho)
  │
  │
  │
  ▼
  Y (alto)
```

- El origen `(0, 0)` está en la **esquina superior izquierda**.
- X crece hacia la derecha.
- Y crece hacia abajo (opuesto a la matemática convencional).
- Un punto se expresa como `(x, y)` → `(columna, fila)`.

### `frame.shape`

Retorna una tupla `(alto, ancho, canales)`.

```python
alto, ancho = frame.shape[:2]
# frame.shape → (480, 640, 3)
# alto  = 480
# ancho = 640
# canales = 3 (BGR)
```

> **Ojo:** en NumPy el orden es `(filas, columnas)` → `(alto, ancho)`,
> pero en las funciones de dibujo de OpenCV los puntos son `(x, y)` → `(ancho, alto)`.
> Es una fuente común de confusión.

### Colores en BGR

OpenCV usa BGR (no RGB). El color se pasa como tupla `(Azul, Verde, Rojo)`, cada canal de 0 a 255.

| Color | BGR |
|---|---|
| Rojo | `(0, 0, 255)` |
| Verde | `(0, 255, 0)` |
| Azul | `(255, 0, 0)` |
| Blanco | `(255, 255, 255)` |
| Negro | `(0, 0, 0)` |
| Amarillo | `(0, 255, 255)` |
| Cian | `(255, 255, 0)` |

---

## Funciones nuevas en este programa

### `cv2.rectangle(img, pt1, pt2, color, thickness)`

Dibuja un rectángulo.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `img` | `ndarray` | Imagen sobre la que se dibuja (se modifica en lugar). |
| `pt1` | `tuple (x, y)` | Esquina superior izquierda. |
| `pt2` | `tuple (x, y)` | Esquina inferior derecha. |
| `color` | `tuple (B, G, R)` | Color del borde. |
| `thickness` | `int` | Grosor del borde en píxeles. `-1` rellena el rectángulo. |

```python
cv2.rectangle(frame, (10, 10), (200, 60), (0, 255, 0), 2)   # borde verde
cv2.rectangle(frame, (10, 10), (200, 60), (0, 255, 0), -1)  # relleno verde
```

---

### `cv2.circle(img, center, radius, color, thickness)`

Dibuja un círculo.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `img` | `ndarray` | Imagen sobre la que se dibuja. |
| `center` | `tuple (x, y)` | Centro del círculo. |
| `radius` | `int` | Radio en píxeles. |
| `color` | `tuple (B, G, R)` | Color. |
| `thickness` | `int` | Grosor del borde. `-1` rellena el círculo. |

```python
cv2.circle(frame, (320, 240), 50, (255, 0, 0), 3)    # borde azul
cv2.circle(frame, (320, 240), 50, (255, 0, 0), -1)   # relleno azul
```

---

### `cv2.line(img, pt1, pt2, color, thickness)`

Dibuja una línea recta entre dos puntos.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `img` | `ndarray` | Imagen sobre la que se dibuja. |
| `pt1` | `tuple (x, y)` | Punto de inicio. |
| `pt2` | `tuple (x, y)` | Punto de fin. |
| `color` | `tuple (B, G, R)` | Color. |
| `thickness` | `int` | Grosor en píxeles. |

```python
cv2.line(frame, (0, 0), (640, 480), (0, 0, 255), 1)   # diagonal roja
```

---

### `cv2.putText(img, text, org, fontFace, fontScale, color, thickness)`

Escribe texto sobre la imagen.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `img` | `ndarray` | Imagen sobre la que se escribe. |
| `text` | `str` | Texto a mostrar. |
| `org` | `tuple (x, y)` | Posición de la **esquina inferior izquierda** del texto. |
| `fontFace` | `int` | Tipo de fuente (constante de OpenCV). |
| `fontScale` | `float` | Escala del tamaño de la fuente. |
| `color` | `tuple (B, G, R)` | Color del texto. |
| `thickness` | `int` | Grosor de los trazos. |

```python
cv2.putText(frame, "Hola", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
```

#### Fuentes disponibles

| Constante | Estilo |
|---|---|
| `cv2.FONT_HERSHEY_SIMPLEX` | Sans-serif normal (la más usada) |
| `cv2.FONT_HERSHEY_PLAIN` | Sans-serif pequeña |
| `cv2.FONT_HERSHEY_DUPLEX` | Sans-serif con doble trazo |
| `cv2.FONT_HERSHEY_COMPLEX` | Serif |
| `cv2.FONT_ITALIC` | Se puede combinar con las anteriores con `\|` |

```python
# Itálica:
cv2.putText(frame, "Hola", (10, 50),
            cv2.FONT_HERSHEY_SIMPLEX | cv2.FONT_ITALIC, 1.0, (255, 255, 255), 2)
```

> **Nota:** el origen `org` es la esquina **inferior** izquierda del texto,
> no la superior. Para posicionar texto en la parte baja de la imagen:
> `(10, alto - 10)` deja un margen de 10px desde el borde inferior.

---

## Comportamiento importante: dibujo en lugar

Todas las funciones de dibujo (`rectangle`, `circle`, `line`, `putText`) **modifican
el array directamente** — no retornan una copia.

```python
# Esto modifica frame:
cv2.rectangle(frame, (10, 10), (200, 60), (0, 255, 0), 2)

# Si se quiere preservar el original:
copia = frame.copy()
cv2.rectangle(copia, (10, 10), (200, 60), (0, 255, 0), 2)
```

---

## Diferencia con programas anteriores

| Aspecto | Prog 01-03 | Prog 04 |
|---|---|---|
| Modifica el frame | No | Sí, dibuja encima |
| Usa `frame.shape` | No | Sí, para calcular posiciones |
| Funciones nuevas | — | `rectangle`, `circle`, `line`, `putText` |

---

## Conceptos clave

- Origen `(0,0)` en esquina superior izquierda; Y crece hacia abajo.
- Colores en BGR, no RGB.
- `thickness = -1` rellena la figura.
- Las funciones de dibujo modifican el array original; usar `.copy()` para preservarlo.
- `frame.shape` retorna `(alto, ancho, canales)` — orden inverso al de los puntos `(x, y)`.
