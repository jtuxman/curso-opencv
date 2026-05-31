# Programa 09 — Redimensionar frame

Permite cambiar el tamaño del frame en tiempo real entre 5 escalas. Presiona `+` para agrandar y `-` para reducir. Muestra la escala activa y las dimensiones reales.

```python
import cv2

cap = cv2.VideoCapture(0)

ancho_original = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
alto_original  = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

escalas = [0.25, 0.5, 1.0, 1.5, 2.0]
indice  = 2   # empieza en 1.0

while True:
    ret, frame = cap.read()

    if not ret:
        break

    escala      = escalas[indice]
    nuevo_ancho = int(ancho_original * escala)
    nuevo_alto  = int(alto_original  * escala)

    if escala < 1.0:
        interpolacion = cv2.INTER_AREA
    else:
        interpolacion = cv2.INTER_LINEAR

    frame_redim = cv2.resize(frame, (nuevo_ancho, nuevo_alto), interpolation=interpolacion)

    etiqueta = f"Escala: {escala}x  ({nuevo_ancho}x{nuevo_alto})"
    cv2.putText(frame_redim, etiqueta, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    cv2.imshow("Redimensionar", frame_redim)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("+") and indice < len(escalas) - 1:
        indice += 1
    elif key == ord("-") and indice > 0:
        indice -= 1
    elif key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
```

---

## Función nueva: `cv2.resize(src, dsize, interpolation)`

Cambia el tamaño de una imagen a las dimensiones indicadas.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `src` | `ndarray` | Imagen de entrada. |
| `dsize` | `tuple (ancho, alto)` | Dimensiones de salida. **Orden: (ancho, alto)**, no (alto, ancho). |
| `interpolation` | `int` | Algoritmo para calcular los píxeles nuevos (ver tabla). |

**Retorna:** `ndarray` — imagen redimensionada. No modifica la original.

**Ejemplos:**

```python
# Tamaño fijo:
pequeño    = cv2.resize(frame, (320, 240))
grande     = cv2.resize(frame, (1280, 720))
miniatura  = cv2.resize(frame, (100, 100))   # cambia la proporción si no es cuadrada

# Por escala (calculando las dimensiones manualmente):
escala = 0.5
nuevo_ancho = int(frame.shape[1] * escala)   # shape[1] = columnas = ancho
nuevo_alto  = int(frame.shape[0] * escala)   # shape[0] = filas    = alto
mitad = cv2.resize(frame, (nuevo_ancho, nuevo_alto))

# ERROR frecuente — orden incorrecto de dimensiones:
cv2.resize(frame, (alto, ancho))    # MAL: da una imagen distorsionada
cv2.resize(frame, (ancho, alto))    # BIEN

# Por qué int() es necesario:
# frame.shape[1] = 640 (int)
# 640 * 0.5 = 320.0 (float) ← resize no acepta float
# int(640 * 0.5) = 320 (int) ← correcto

# Redimensionar y mantener la proporción (aspect ratio):
alto_deseado = 200
factor = alto_deseado / frame.shape[0]
nuevo_ancho = int(frame.shape[1] * factor)
redim = cv2.resize(frame, (nuevo_ancho, alto_deseado))
```

---

## Métodos de interpolación

La interpolación define cómo se calculan los nuevos píxeles al cambiar el tamaño.

### Al reducir (escala < 1.0)

```
Original 4x4:              Reducido 2x2 con INTER_AREA:
[10][20][30][40]           [15][35]   ← promedio de bloques 2x2
[50][60][70][80]   →       [55][75]
[11][21][31][41]
[51][61][71][81]
```

`INTER_AREA` promedia los píxeles que "desaparecen", produciendo una imagen suave sin aliasing.

### Al agrandar (escala > 1.0)

```
Original 2x2:         Agrandado 4x4 con INTER_LINEAR:
[10][20]       →      [10][13][17][20]   ← interpolación lineal entre vecinos
[50][60]              [22][26][30][33]
                      [38][41][45][48]
                      [50][53][57][60]
```

`INTER_LINEAR` interpola entre píxeles vecinos para suavizar la ampliación.

### Comparación completa

| Constante | Para | Velocidad | Calidad | Cuándo usar |
|---|---|---|---|---|
| `cv2.INTER_NEAREST` | Ambos | Muy rápida | Baja | Prototipado, pixel art, máscaras binarias |
| `cv2.INTER_LINEAR` | Agrandar | Rápida | Buena | **Tiempo real, escala > 1** |
| `cv2.INTER_AREA` | Reducir | Media | Muy buena | **Tiempo real, escala < 1** |
| `cv2.INTER_CUBIC` | Agrandar | Lenta | Alta | Ampliación de alta calidad |
| `cv2.INTER_LANCZOS4` | Ambos | Muy lenta | Muy alta | Máxima calidad, sin restricción de tiempo |

```python
# Regla práctica del programa:
if escala < 1.0:
    inter = cv2.INTER_AREA      # reducir → AREA para evitar aliasing
else:
    inter = cv2.INTER_LINEAR    # agrandar → LINEAR para suavidad

# Para máxima calidad sin importar la velocidad:
if escala < 1.0:
    inter = cv2.INTER_AREA
else:
    inter = cv2.INTER_CUBIC     # mejor que LINEAR, más lento

# Para máxima velocidad (prototipos):
inter = cv2.INTER_NEAREST      # siempre, sin importar la escala
```

---

## Concepto: relación entre `frame.shape` y `resize`

Es la misma confusión que en el dibujo pero ahora es crítico para `resize`:

```python
# frame.shape retorna (filas, columnas, canales) = (alto, ancho, canales)
alto,  ancho  = frame.shape[:2]   # alto=480, ancho=640

# cv2.resize espera (ancho, alto) como dsize:
cv2.resize(frame, (ancho, alto))   # BIEN: (640, 480)
cv2.resize(frame, (alto,  ancho))  # MAL:  (480, 640) → imagen girada/distorsionada
```

---

## Patrón de navegación con límites

A diferencia del ciclo infinito del programa 05 (con `%`), aquí se limita el índice dentro del rango de la lista:

```python
# Avanzar (no pasar del último):
if key == ord("+") and indice < len(escalas) - 1:
    indice += 1
# Con escalas = [0.25, 0.5, 1.0, 1.5, 2.0] (5 elementos):
# len(escalas) - 1 = 4
# Si indice=4 y se presiona '+', la condición es False → no cambia

# Retroceder (no bajar de 0):
elif key == ord("-") and indice > 0:
    indice -= 1
# Si indice=0 y se presiona '-', la condición es False → no cambia
```

Comparación de patrones:

```python
# Ciclo infinito (programa 05 — N estados que se repiten):
indice = (indice + 1) % len(lista)   # 0→1→2→3→0→1→...

# Con límites (programa 09 — rango acotado con extremos):
if indice < len(lista) - 1: indice += 1   # para en el último
if indice > 0:              indice -= 1   # para en el primero
```

---

## Conceptos clave

- `cv2.resize()` recibe `(ancho, alto)` — **no** `(alto, ancho)`.
- Usar `INTER_AREA` para reducir y `INTER_LINEAR` para agrandar.
- Convertir siempre a `int()` las dimensiones calculadas con escala flotante.
- `frame.shape` retorna `(alto, ancho)` — orden inverso al que espera `resize`.
- El patrón con límites evita salirse del rango de la lista, a diferencia del ciclo con `%`.
