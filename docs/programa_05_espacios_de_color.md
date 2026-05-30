# Programa 05 — Espacios de color

Permite cambiar en tiempo real entre cuatro espacios de color pulsando `m`. Muestra el nombre del modo activo sobre el frame. Presiona `q` para salir.

```python
import cv2

cap = cv2.VideoCapture(0)

modos = ["BGR", "Gris", "HSV", "LAB"]
modo_actual = 0

print("Presiona 'm' para cambiar modo, 'q' para salir")

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

Un **espacio de color** es una forma de representar el color de un píxel usando números.
El mismo color puede describirse de distintas maneras según el espacio usado.

### BGR (predeterminado en OpenCV)

Igual que RGB pero con los canales invertidos: Azul, Verde, Rojo.

```
Píxel = (B, G, R)   cada canal de 0 a 255
```

Es el espacio con el que trabaja OpenCV internamente. Toda imagen leída con `cap.read()`
o `cv2.imread()` llega en BGR.

---

### Escala de grises (GRAY)

Un solo canal. Cada píxel es un valor de intensidad luminosa de 0 (negro) a 255 (blanco).

```
Píxel = L   (0-255)
```

Se calcula como una combinación ponderada de los canales BGR:

```
L = 0.114·B + 0.587·G + 0.299·R
```

El verde tiene más peso porque el ojo humano es más sensible a él.

---

### HSV (Hue, Saturation, Value)

Separa el **color** (matiz) de la **luminosidad**, lo que lo hace muy útil para
detectar colores específicos aunque cambien las condiciones de luz.

```
Píxel = (H, S, V)
```

| Canal | Nombre | Rango en OpenCV | Descripción |
|---|---|---|---|
| H | Matiz (Hue) | 0 – 179 | El color puro: rojo, verde, azul... |
| S | Saturación | 0 – 255 | Qué tan "vivo" es el color (0 = gris) |
| V | Valor (brillo) | 0 – 255 | Qué tan claro u oscuro |

> **Ojo:** en otros programas H va de 0 a 360. En OpenCV va de 0 a 179
> (se divide entre 2 para caber en un byte).

HSV es el espacio preferido para **detectar objetos por color** con `cv2.inRange()`.

---

### LAB (L\*a\*b\*)

Diseñado para aproximarse a la percepción humana del color. Separa luminosidad
de crominancia.

```
Píxel = (L, a, b)
```

| Canal | Descripción |
|---|---|
| L | Luminosidad (0=negro, 255=blanco) |
| a | Verde (−) ↔ Rojo (+) |
| b | Azul (−) ↔ Amarillo (+) |

Es útil para comparar colores de forma perceptualmente uniforme (dos colores
que se ven distintos al ojo tienen distancia LAB grande).

---

## Función nueva: `cv2.cvtColor(src, code)`

Convierte una imagen de un espacio de color a otro.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `src` | `ndarray` | Imagen de entrada. |
| `code` | `int` | Constante que indica la conversión a realizar. |

**Retorna:** `ndarray` — imagen convertida (no modifica la original).

```python
gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
hsv  = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
lab  = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
rgb  = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)   # para usar con matplotlib/Pillow
```

#### Códigos de conversión más usados

| Código | De → A |
|---|---|
| `cv2.COLOR_BGR2GRAY` | BGR → Escala de grises |
| `cv2.COLOR_GRAY2BGR` | Grises → BGR (para poder dibujar encima) |
| `cv2.COLOR_BGR2HSV` | BGR → HSV |
| `cv2.COLOR_HSV2BGR` | HSV → BGR |
| `cv2.COLOR_BGR2LAB` | BGR → LAB |
| `cv2.COLOR_LAB2BGR` | LAB → BGR |
| `cv2.COLOR_BGR2RGB` | BGR → RGB (para matplotlib, Pillow, etc.) |

---

## Por qué se hace doble conversión para el modo gris

```python
salida = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)   # (alto, ancho) — 1 canal
salida = cv2.cvtColor(salida, cv2.COLOR_GRAY2BGR)  # (alto, ancho, 3) — 3 canales
```

`cv2.imshow()` puede mostrar imágenes de 1 canal (gris) o 3 canales (BGR).
El problema es que `cv2.putText()` necesita 3 canales para que el color del texto
funcione correctamente. La segunda conversión devuelve la imagen a 3 canales
(visualmente sigue siendo gris) para poder escribir el texto encima.

---

## Patrón: ciclo de modos con lista y módulo

```python
modos = ["BGR", "Gris", "HSV", "LAB"]
modo_actual = 0

# Al presionar 'm':
modo_actual = (modo_actual + 1) % len(modos)
```

El operador `%` (módulo) hace que el índice vuelva a 0 al llegar al final de la lista.
Es un patrón reutilizable para ciclar entre cualquier conjunto de opciones.

---

## Diferencia con programas anteriores

| Aspecto | Prog 01-04 | Prog 05 |
|---|---|---|
| Espacio de color | Solo BGR | BGR, Gris, HSV, LAB |
| Cambio en tiempo real | No aplica | Tecla `m` cicla entre modos |
| Función nueva | — | `cv2.cvtColor()` |

---

## Conceptos clave

- OpenCV trabaja en BGR por defecto, no RGB.
- `cv2.cvtColor()` no modifica la imagen original, retorna una nueva.
- HSV es el espacio más útil para detectar colores por rango.
- Gris tiene 1 canal; convertir de vuelta a BGR con `COLOR_GRAY2BGR` antes de dibujar texto.
- El patrón `(indice + 1) % len(lista)` cicla indefinidamente por una lista.
