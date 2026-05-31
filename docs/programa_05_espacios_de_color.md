# Programa 05 — Espacios de color

Permite cambiar en tiempo real entre cuatro espacios de color pulsando `m`. Muestra el nombre del modo activo sobre el frame.

```python
import cv2

cap = cv2.VideoCapture(0)

modos = ["BGR", "Gris", "HSV", "LAB"]
modo_actual = 0

while True:
    ret, frame = cap.read()

    if not ret:
        break

    modo = modos[modo_actual]

    if modo == "Gris":
        salida = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        salida = cv2.cvtColor(salida, cv2.COLOR_GRAY2BGR)
    elif modo == "HSV":
        salida = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    elif modo == "LAB":
        salida = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    else:
        salida = frame

    cv2.putText(salida, f"Modo: {modo}  (M = cambiar)", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow("Espacios de color", salida)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("m"):
        modo_actual = (modo_actual + 1) % len(modos)
    elif key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
```

---

## Concepto clave: espacios de color

Un **espacio de color** es un modelo matemático que describe cómo representar un color usando números. El mismo color físico se puede describir de formas distintas según el espacio usado, cada uno con ventajas para diferentes tareas.

### BGR (predeterminado en OpenCV)

Igual que RGB pero con los canales en orden invertido: **B**lue (Azul), **G**reen (Verde), **R**ed (Rojo).

```
Píxel BGR = (B, G, R)   cada canal: 0–255
Ejemplo:   (0, 255, 0)  = verde puro
           (255, 0, 0)  = azul puro
           (0, 0, 255)  = rojo puro
```

> OpenCV usa BGR por razones históricas (los primeros sistemas de visión guardaban los bytes en ese orden). Toda imagen leída con `cap.read()` o `cv2.imread()` llega en BGR.

### Escala de grises (GRAY)

Un solo canal. Cada píxel representa la **intensidad luminosa**: 0 = negro, 255 = blanco.

```
Píxel GRAY = L   (0–255)
```

Se calcula con una fórmula ponderada que simula la sensibilidad del ojo humano:

```
L = 0.114·B + 0.587·G + 0.299·R
```

El canal verde tiene más peso porque el ojo humano es más sensible al verde.

### HSV (Hue, Saturation, Value)

Separa el **color** (Hue/Matiz) de la **luminosidad** (Value), haciéndolo muy útil para detectar colores específicos bajo diferentes condiciones de luz.

```
Píxel HSV = (H, S, V)
```

| Canal | Nombre | Rango en OpenCV | Qué representa |
|---|---|---|---|
| H | Hue / Matiz | 0 – 179 | El color en sí: rojo=0, amarillo=30, verde=60, cian=90, azul=120, magenta=150 |
| S | Saturation | 0 – 255 | Intensidad del color: 0=gris, 255=color puro |
| V | Value / Brillo | 0 – 255 | Brillo: 0=negro, 255=máximo brillo |

> **Ojo:** en la mayoría de herramientas H va de 0° a 360°. En OpenCV va de 0 a 179 (se divide entre 2 para que quepa en un byte de 8 bits).

```python
# Ejemplo: detectar objetos rojos con inRange en HSV:
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
limite_bajo = (0, 100, 100)    # H=0 (rojo), S y V mínimos
limite_alto = (10, 255, 255)   # H=10 (sigue siendo rojo), S y V máximos
mascara = cv2.inRange(hsv, limite_bajo, limite_alto)
```

### LAB (L\*a\*b\*)

Diseñado para aproximarse a la **percepción humana** del color. Separa luminosidad de información de color.

```
Píxel LAB = (L, a, b)
```

| Canal | Rango en OpenCV | Qué representa |
|---|---|---|
| L | 0 – 255 | Luminosidad (0=negro, 255=blanco) |
| a | 0 – 255 (centrado en 128) | Verde (bajo) ↔ Rojo (alto) |
| b | 0 – 255 (centrado en 128) | Azul (bajo) ↔ Amarillo (alto) |

Es útil cuando se necesita medir la **diferencia visual** entre dos colores tal como los percibe el ojo humano.

---

## Función nueva: `cv2.cvtColor(src, code)`

Convierte una imagen de un espacio de color a otro.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `src` | `ndarray` | Imagen de entrada. |
| `code` | `int` | Constante que indica la conversión (`cv2.COLOR_origen2destino`). |

**Retorna:** `ndarray` — imagen convertida. **No modifica la imagen original.**

**Ejemplos:**

```python
# Conversiones más comunes desde BGR:
gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)    # BGR → 1 canal gris
hsv  = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)     # BGR → HSV
lab  = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)     # BGR → LAB
rgb  = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)     # BGR → RGB (para matplotlib/Pillow)

# Conversiones inversas (volver a BGR):
bgr_desde_hsv  = cv2.cvtColor(hsv,  cv2.COLOR_HSV2BGR)
bgr_desde_lab  = cv2.cvtColor(lab,  cv2.COLOR_LAB2BGR)
bgr_desde_gris = cv2.cvtColor(gris, cv2.COLOR_GRAY2BGR)   # sigue siendo gris visualmente

# Conversión a través de múltiples espacios:
# BGR → GRAY → BGR (para dibujar texto en color sobre imagen gris):
gris       = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
gris_3ch   = cv2.cvtColor(gris,  cv2.COLOR_GRAY2BGR)
cv2.putText(gris_3ch, "Texto", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

# Verificar cuántos canales tiene una imagen:
print(frame.shape)      # → (480, 640, 3)  — 3 canales BGR
print(gris.shape)       # → (480, 640)     — 1 canal gris
print(gris_3ch.shape)   # → (480, 640, 3)  — 3 canales (gris en BGR)
```

#### Códigos de conversión más usados

| Código | De → A | Canales entrada → salida |
|---|---|---|
| `cv2.COLOR_BGR2GRAY` | BGR → Grises | 3 → 1 |
| `cv2.COLOR_GRAY2BGR` | Grises → BGR | 1 → 3 |
| `cv2.COLOR_BGR2HSV` | BGR → HSV | 3 → 3 |
| `cv2.COLOR_HSV2BGR` | HSV → BGR | 3 → 3 |
| `cv2.COLOR_BGR2LAB` | BGR → LAB | 3 → 3 |
| `cv2.COLOR_LAB2BGR` | LAB → BGR | 3 → 3 |
| `cv2.COLOR_BGR2RGB` | BGR → RGB | 3 → 3 |
| `cv2.COLOR_RGB2BGR` | RGB → BGR | 3 → 3 |

---

## Por qué se hace doble conversión para el modo gris

```python
salida = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)   # (alto, ancho)    — 1 canal
salida = cv2.cvtColor(salida, cv2.COLOR_GRAY2BGR)  # (alto, ancho, 3) — 3 canales
```

El problema si no se hace la segunda conversión:

```python
# Imagen gris de 1 canal + putText:
gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
cv2.putText(gris, "Hola", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
# El color (0, 255, 0) verde se ignora — el texto sale blanco porque
# una imagen de 1 canal solo puede tener intensidad, no color
# Además en algunas versiones de OpenCV puede causar error
```

La doble conversión resuelve esto: la imagen sigue viéndose gris visualmente, pero tiene 3 canales, lo que permite dibujar texto en color correctamente.

---

## Patrón: ciclo de modos con lista y módulo

```python
modos = ["BGR", "Gris", "HSV", "LAB"]
modo_actual = 0

# Al presionar 'm':
modo_actual = (modo_actual + 1) % len(modos)
# Iteración:  0 → 1 → 2 → 3 → 0 → 1 → ...
#             BGR  Gris HSV LAB BGR  Gris
```

El operador `%` (módulo) retorna el resto de la división. Cuando `modo_actual + 1` llega a `len(modos)` (= 4), `4 % 4 = 0`, volviendo al inicio.

---

## Cuándo usar cada espacio

| Tarea | Espacio recomendado | Por qué |
|---|---|---|
| Pre-procesado general | GRAY | Más rápido, menos memoria |
| Detección de bordes (Canny) | GRAY | Canny requiere 1 canal |
| Detección de color por rango | HSV | Separa color de brillo |
| Comparar similitud visual | LAB | Simula percepción humana |
| Procesar con matplotlib/Pillow | RGB | Esas librerías esperan RGB |

---

## Conceptos clave

- OpenCV trabaja en BGR por defecto, no RGB.
- `cv2.cvtColor()` retorna una imagen nueva; no modifica la original.
- Gris tiene 1 canal; convertir a BGR con `COLOR_GRAY2BGR` antes de dibujar texto en color.
- HSV es el espacio más útil para detectar colores por rango con `inRange()`.
- El patrón `(indice + 1) % len(lista)` cicla indefinidamente por una lista.
