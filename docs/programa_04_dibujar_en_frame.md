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

## Concepto previo: sistema de coordenadas y colores

### Sistema de coordenadas

```
(0,0) ──────────────────────► X (ancho, columnas)
  │    (10,10)
  │       ┌──────────────┐
  │       │              │
  │       └──────────────┘ (200,60)
  │
  ▼
  Y (alto, filas)
```

- El origen `(0, 0)` está en la **esquina superior izquierda**.
- **X** crece hacia la **derecha** (columnas del array NumPy).
- **Y** crece hacia **abajo** (filas del array NumPy) — opuesto a la matemática.
- Un punto se expresa como `(x, y)` = `(columna, fila)`.

> **Confusión frecuente:** `frame.shape` retorna `(filas, columnas)` = `(alto, ancho)`,
> pero las funciones de dibujo usan puntos `(x, y)` = `(ancho, alto)`.
> Son el mismo dato pero en orden invertido.
>
> ```python
> alto, ancho = frame.shape[:2]   # shape: (alto, ancho)
> centro = (ancho // 2, alto // 2)  # punto: (x, y) = (ancho, alto)
> ```

### Colores en BGR

OpenCV usa BGR (Azul, Verde, Rojo), **no** RGB. Cada canal va de 0 a 255.

```python
# Colores básicos:
VERDE   = (0, 255, 0)      # B=0,   G=255, R=0
AZUL    = (255, 0, 0)      # B=255, G=0,   R=0
ROJO    = (0, 0, 255)      # B=0,   G=0,   R=255
BLANCO  = (255, 255, 255)
NEGRO   = (0, 0, 0)
AMARILLO = (0, 255, 255)   # B=0,   G=255, R=255
CIAN    = (255, 255, 0)    # B=255, G=255, R=0
MAGENTA = (255, 0, 255)    # B=255, G=0,   R=255
NARANJA = (0, 165, 255)    # B=0,   G=165, R=255
GRIS    = (128, 128, 128)
```

### `frame.shape`

Retorna las dimensiones del array como tupla `(filas, columnas, canales)`.

```python
alto, ancho = frame.shape[:2]
# frame.shape → (480, 640, 3)
# alto    = 480  (filas)
# ancho   = 640  (columnas)
# canales = 3    (B, G, R)

# Para imagen en escala de grises:
alto, ancho = gris.shape     # solo 2 dimensiones: (filas, columnas)
# gris.shape → (480, 640)    # sin el tercer valor de canales
```

---

## Funciones nuevas en este programa

### `cv2.rectangle(img, pt1, pt2, color, thickness)`

Dibuja un rectángulo. **Modifica `img` directamente (en lugar).**

| Parámetro | Tipo | Descripción |
|---|---|---|
| `img` | `ndarray` | Imagen sobre la que se dibuja. Se modifica en lugar. |
| `pt1` | `tuple (x, y)` | Esquina superior izquierda del rectángulo. |
| `pt2` | `tuple (x, y)` | Esquina inferior derecha del rectángulo. |
| `color` | `tuple (B, G, R)` | Color del borde o relleno. |
| `thickness` | `int` | Grosor del borde en píxeles. `-1` rellena el rectángulo completo. |

**Ejemplos:**

```python
# Rectángulo con borde:
cv2.rectangle(frame, (10, 10), (200, 60), (0, 255, 0), 2)    # borde verde de 2px

# Rectángulo relleno (grosor -1):
cv2.rectangle(frame, (10, 10), (200, 60), (0, 255, 0), -1)   # relleno verde

# Rectángulo semitransparente (técnica con overlay):
overlay = frame.copy()
cv2.rectangle(overlay, (10, 10), (200, 60), (0, 0, 0), -1)   # negro relleno
alpha = 0.4  # 40% de opacidad
cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

# Rectángulo que ocupa toda la imagen:
h, w = frame.shape[:2]
cv2.rectangle(frame, (0, 0), (w, h), (0, 0, 255), 3)  # borde rojo alrededor

# Usar para marcar regiones de interés (ROI):
x, y, w, h = 100, 100, 200, 150   # región a marcar
cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
```

---

### `cv2.circle(img, center, radius, color, thickness)`

Dibuja un círculo. **Modifica `img` directamente.**

| Parámetro | Tipo | Descripción |
|---|---|---|
| `img` | `ndarray` | Imagen sobre la que se dibuja. |
| `center` | `tuple (x, y)` | Coordenadas del centro del círculo. |
| `radius` | `int` | Radio del círculo en píxeles. |
| `color` | `tuple (B, G, R)` | Color. |
| `thickness` | `int` | Grosor del borde. `-1` rellena el círculo. |

**Ejemplos:**

```python
alto, ancho = frame.shape[:2]
cx, cy = ancho // 2, alto // 2   # centro del frame

# Círculo en el centro con borde azul:
cv2.circle(frame, (cx, cy), 50, (255, 0, 0), 3)

# Círculo relleno rojo:
cv2.circle(frame, (cx, cy), 30, (0, 0, 255), -1)

# Punto (círculo muy pequeño):
cv2.circle(frame, (100, 100), 3, (0, 255, 0), -1)   # punto verde de 3px

# Varios círculos concéntricos:
for radio in [20, 40, 60, 80]:
    cv2.circle(frame, (cx, cy), radio, (0, 255, 0), 1)

# Marcar puntos detectados (landmarks, esquinas, etc.):
puntos = [(50, 50), (100, 80), (200, 120)]
for px, py in puntos:
    cv2.circle(frame, (px, py), 5, (0, 0, 255), -1)
```

---

### `cv2.line(img, pt1, pt2, color, thickness)`

Dibuja una línea recta entre dos puntos. **Modifica `img` directamente.**

| Parámetro | Tipo | Descripción |
|---|---|---|
| `img` | `ndarray` | Imagen sobre la que se dibuja. |
| `pt1` | `tuple (x, y)` | Punto de inicio de la línea. |
| `pt2` | `tuple (x, y)` | Punto de fin de la línea. |
| `color` | `tuple (B, G, R)` | Color. |
| `thickness` | `int` | Grosor en píxeles. |

**Ejemplos:**

```python
alto, ancho = frame.shape[:2]

# Línea diagonal de esquina a esquina:
cv2.line(frame, (0, 0), (ancho, alto), (0, 0, 255), 1)

# Línea horizontal en el centro:
cy = alto // 2
cv2.line(frame, (0, cy), (ancho, cy), (255, 255, 0), 2)

# Línea vertical en el centro:
cx = ancho // 2
cv2.line(frame, (cx, 0), (cx, alto), (255, 255, 0), 2)

# Cruz en el centro del frame:
cv2.line(frame, (0, cy), (ancho, cy), (0, 255, 255), 1)   # horizontal
cv2.line(frame, (cx, 0), (cx, alto), (0, 255, 255), 1)   # vertical

# Líneas para conectar puntos detectados:
puntos = [(50, 50), (150, 100), (300, 80)]
for i in range(len(puntos) - 1):
    cv2.line(frame, puntos[i], puntos[i+1], (0, 255, 0), 2)
```

---

### `cv2.putText(img, text, org, fontFace, fontScale, color, thickness)`

Escribe texto sobre la imagen. **Modifica `img` directamente.**

| Parámetro | Tipo | Descripción |
|---|---|---|
| `img` | `ndarray` | Imagen sobre la que se escribe. |
| `text` | `str` | Texto a mostrar. Solo caracteres ASCII (sin tildes ni ñ). |
| `org` | `tuple (x, y)` | Posición de la **esquina inferior izquierda** del texto. |
| `fontFace` | `int` | Tipo de fuente. |
| `fontScale` | `float` | Factor de escala del tamaño. `1.0` = tamaño base, `0.5` = mitad. |
| `color` | `tuple (B, G, R)` | Color del texto. |
| `thickness` | `int` | Grosor de los trazos. |

**Ejemplos:**

```python
alto, ancho = frame.shape[:2]

# Texto en la parte superior:
cv2.putText(frame, "Hola mundo", (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)

# Texto en la parte inferior (org es la esquina INFERIOR izquierda):
cv2.putText(frame, "Presiona Q para salir", (10, alto - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

# Texto con fondo negro para mejor legibilidad:
texto = "Estado: activo"
# Calcular el tamaño del texto para dibujar el fondo:
(tw, th), _ = cv2.getTextSize(texto, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
cv2.rectangle(frame, (8, 8), (tw + 12, th + 16), (0, 0, 0), -1)  # fondo negro
cv2.putText(frame, texto, (10, th + 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

# Texto centrado horizontalmente:
texto = "CENTRADO"
(tw, th), _ = cv2.getTextSize(texto, cv2.FONT_HERSHEY_SIMPLEX, 1.0, 2)
x_centro = (ancho - tw) // 2
cv2.putText(frame, texto, (x_centro, 50),
            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
```

> **Limitación importante:** `putText` solo soporta caracteres ASCII.
> Las tildes (á, é, í, ó, ú) y la ñ **no** se muestran correctamente.
> Para mostrar texto con esos caracteres se necesita Pillow/PIL:
> ```python
> # Con Pillow (soporta tildes y ñ):
> from PIL import Image, ImageDraw, ImageFont
> img_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
> draw = ImageDraw.Draw(img_pil)
> draw.text((10, 10), "Cámara activa", fill=(255, 255, 255))
> frame = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
> ```

#### Fuentes disponibles

| Constante | Estilo | Apariencia |
|---|---|---|
| `cv2.FONT_HERSHEY_SIMPLEX` | Sans-serif regular | La más usada, limpia |
| `cv2.FONT_HERSHEY_PLAIN` | Sans-serif pequeña | Para texto pequeño |
| `cv2.FONT_HERSHEY_DUPLEX` | Sans-serif gruesa | Más visible |
| `cv2.FONT_HERSHEY_COMPLEX` | Serif | Más formal |
| `cv2.FONT_HERSHEY_TRIPLEX` | Serif gruesa | Muy visible |
| `cv2.FONT_ITALIC` | Modificador itálico | Combinar con `\|` |

```python
# Itálica combinada:
cv2.putText(frame, "Texto", (10, 50),
            cv2.FONT_HERSHEY_SIMPLEX | cv2.FONT_ITALIC, 1.0, (255, 255, 255), 2)
```

---

## Comportamiento importante: modificación en lugar (in-place)

Todas las funciones de dibujo **modifican el array original directamente**:

```python
# Esto modifica frame de forma permanente:
cv2.rectangle(frame, (10, 10), (200, 60), (0, 255, 0), 2)
cv2.circle(frame, (320, 240), 50, (255, 0, 0), 3)
# Ya no es posible recuperar el frame sin el rectángulo o el círculo

# Si se necesita preservar el original, copiar ANTES de dibujar:
frame_original = frame.copy()   # copia independiente
frame_dibujo   = frame.copy()
cv2.rectangle(frame_dibujo, (10, 10), (200, 60), (0, 255, 0), 2)

cv2.imshow("Original", frame_original)   # sin dibujos
cv2.imshow("Dibujo",   frame_dibujo)     # con dibujos
```

---

## Conceptos clave

- Origen `(0, 0)` en la esquina superior izquierda; Y crece hacia abajo.
- `frame.shape` retorna `(alto, ancho)` — orden inverso al de los puntos `(x, y)`.
- Colores en **BGR**, no RGB.
- `thickness = -1` rellena la figura.
- Las funciones de dibujo **modifican el array original**; usar `.copy()` si se necesita preservarlo.
- `putText` no soporta tildes ni ñ; usar Pillow para texto con caracteres especiales.
