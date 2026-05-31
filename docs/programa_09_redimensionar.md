# Programa 09 — Redimensionar frame

Permite cambiar el tamaño del frame en tiempo real entre 5 escalas predefinidas. Presiona `+` para agrandar y `-` para reducir. Muestra la escala activa y las dimensiones reales en pantalla.

```python
import cv2

cap = cv2.VideoCapture(0)

ancho_original = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
alto_original  = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

escalas = [0.25, 0.5, 1.0, 1.5, 2.0]
indice  = 2  # empieza en 1.0

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

Cambia el tamaño de una imagen.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `src` | `ndarray` | Imagen de entrada. |
| `dsize` | `tuple (ancho, alto)` | Dimensiones de salida en píxeles. |
| `interpolation` | `int` | Algoritmo de interpolación (ver tabla). |

**Retorna:** `ndarray` — imagen redimensionada (no modifica la original).

```python
# Tamaño fijo:
pequeño = cv2.resize(frame, (320, 240))

# Por escala (calcular dimensiones primero):
nuevo_ancho = int(frame.shape[1] * 0.5)
nuevo_alto  = int(frame.shape[0] * 0.5)
mitad = cv2.resize(frame, (nuevo_ancho, nuevo_alto))
```

> **Importante:** `dsize` es `(ancho, alto)` — orden inverso a `frame.shape`
> que retorna `(alto, ancho)`. El mismo patrón que en `VideoWriter`.

---

## Métodos de interpolación

Cuando se redimensiona una imagen, los píxeles nuevos deben calcularse a partir
de los existentes. El método de interpolación define cómo se hace ese cálculo.

| Constante | Cuándo usar | Velocidad | Calidad |
|---|---|---|---|
| `cv2.INTER_NEAREST` | Prototipado rápido, pixel art | Muy rápida | Baja |
| `cv2.INTER_LINEAR` | **Agrandar** (escala > 1) | Rápida | Buena |
| `cv2.INTER_AREA` | **Reducir** (escala < 1) | Media | Muy buena |
| `cv2.INTER_CUBIC` | Agrandar con alta calidad | Lenta | Alta |
| `cv2.INTER_LANCZOS4` | Máxima calidad | Muy lenta | Muy alta |

### Regla práctica

```python
if escala < 1.0:
    interpolacion = cv2.INTER_AREA     # reducir → AREA evita aliasing
else:
    interpolacion = cv2.INTER_LINEAR   # agrandar → LINEAR es suficiente
```

**¿Por qué importa?**

- Al **reducir** con `INTER_LINEAR` aparece *aliasing* (efecto de escalera/moiré).
  `INTER_AREA` promedia los píxeles vecinos y produce una imagen más suave.
- Al **agrandar** con `INTER_AREA` el resultado se ve borroso.
  `INTER_LINEAR` interpola entre píxeles adyacentes y da mejor resultado.

---

## Cómo se calculan las nuevas dimensiones

```python
escala      = 0.5
nuevo_ancho = int(ancho_original * escala)   # 640 * 0.5 = 320
nuevo_alto  = int(alto_original  * escala)   # 480 * 0.5 = 240
```

Se usa `int()` porque `resize` requiere enteros, y la multiplicación con float
puede producir un número con decimales (ej. `319.9`).

---

## Navegación por lista con límites

```python
if key == ord("+") and indice < len(escalas) - 1:
    indice += 1
elif key == ord("-") and indice > 0:
    indice -= 1
```

A diferencia del programa 05 (que ciclaba con `%`), aquí se limita el índice
entre `0` y `len(escalas) - 1` para no salir del rango de la lista.

| Patrón | Comportamiento |
|---|---|
| `(indice + 1) % len(lista)` | Cicla: al llegar al final vuelve al inicio |
| `if indice < len(lista) - 1: indice += 1` | Para en el último elemento |

---

## Diferencia con programas anteriores

| Aspecto | Prog 01-08 | Prog 09 |
|---|---|---|
| Tamaño del frame | Fijo (el de la cámara) | Variable con `+` y `-` |
| Función nueva | — | `cv2.resize()` |
| Interpolación | No aplica | `INTER_AREA` o `INTER_LINEAR` según escala |
| Navegación por lista | Ciclo (`%`) o booleano | Con límites min/max |

---

## Conceptos clave

- `cv2.resize()` recibe `(ancho, alto)` — no `(alto, ancho)`.
- Usar `INTER_AREA` para reducir y `INTER_LINEAR` para agrandar.
- Convertir siempre a `int()` las dimensiones calculadas con escala flotante.
- El patrón con límites (`indice > 0`, `indice < len - 1`) evita salirse de la lista.
