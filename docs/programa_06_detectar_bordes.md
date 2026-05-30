# Programa 06 — Detección de bordes con Canny

Detecta bordes en tiempo real usando el algoritmo Canny. Presiona `m` para alternar entre la imagen original y los bordes detectados. Presiona `q` para salir.

```python
import cv2

cap = cv2.VideoCapture(0)

umbral1 = 50
umbral2 = 150

mostrar_bordes = True

while True:
    ret, frame = cap.read()

    if not ret:
        break

    gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gris = cv2.GaussianBlur(gris, (5, 5), 0)
    bordes = cv2.Canny(gris, umbral1, umbral2)

    if mostrar_bordes:
        salida = cv2.cvtColor(bordes, cv2.COLOR_GRAY2BGR)
        etiqueta = f"Canny  umbral1={umbral1}  umbral2={umbral2}"
    else:
        salida = frame
        etiqueta = "Original"

    cv2.putText(salida, etiqueta, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("Deteccion de bordes", salida)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("m"):
        mostrar_bordes = not mostrar_bordes
    elif key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
```

---

## Concepto: ¿qué es un borde?

Un **borde** en una imagen es una zona donde la intensidad de los píxeles cambia
bruscamente. Por ejemplo, el límite entre un objeto oscuro y un fondo claro.

Canny detecta esos cambios calculando el **gradiente** (la derivada) de la imagen:
zonas con gradiente alto son bordes.

---

## Pipeline del programa (3 pasos antes de Canny)

```
frame (BGR)
    │
    ▼
cv2.cvtColor → gris (1 canal)
    │
    ▼
cv2.GaussianBlur → gris suavizado
    │
    ▼
cv2.Canny → bordes (blanco/negro)
```

El suavizado previo es fundamental: sin él, el ruido de la cámara genera
cientos de falsos bordes.

---

## Funciones nuevas en este programa

### `cv2.GaussianBlur(src, ksize, sigmaX)`

Aplica un desenfoque gaussiano para suavizar la imagen y reducir ruido.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `src` | `ndarray` | Imagen de entrada. |
| `ksize` | `tuple (ancho, alto)` | Tamaño del kernel. Debe ser impar y positivo: `(3,3)`, `(5,5)`, `(7,7)`... |
| `sigmaX` | `float` | Desviación estándar en X. `0` = calculada automáticamente desde `ksize`. |

**Retorna:** `ndarray` — imagen suavizada.

```python
suave = cv2.GaussianBlur(gris, (5, 5), 0)   # kernel 5x5
suave = cv2.GaussianBlur(gris, (11, 11), 0) # más suave
suave = cv2.GaussianBlur(gris, (3, 3), 0)   # menos suave
```

> **Regla del kernel:** cuanto mayor el tamaño, más suavizado pero más lento.
> Para detección de bordes en tiempo real `(5, 5)` es un buen balance.
> El tamaño siempre debe ser **impar** (3, 5, 7, 9...).

---

### `cv2.Canny(image, threshold1, threshold2)`

Detecta bordes usando el algoritmo de Canny (1986).

| Parámetro | Tipo | Descripción |
|---|---|---|
| `image` | `ndarray` | Imagen en escala de grises. |
| `threshold1` | `float` | Umbral inferior (hysteresis). |
| `threshold2` | `float` | Umbral superior (hysteresis). |

**Retorna:** `ndarray` — imagen binaria: bordes en blanco (255), fondo en negro (0).

```python
bordes = cv2.Canny(gris, 50, 150)
```

#### Cómo funcionan los umbrales (hysteresis)

Canny clasifica los píxeles en tres categorías:

| Gradiente del píxel | Resultado |
|---|---|
| Mayor que `threshold2` | Borde fuerte — siempre incluido |
| Entre `threshold1` y `threshold2` | Borde débil — incluido solo si conecta con un borde fuerte |
| Menor que `threshold1` | Descartado |

```
threshold1=50   threshold2=150

  0 ──── 50 ──────────── 150 ──► gradiente
  │       │               │
descarte  débil          fuerte
```

#### Guía para elegir umbrales

| Situación | threshold1 | threshold2 |
|---|---|---|
| Detectar muchos bordes (sensible) | 20 | 60 |
| Balance general | 50 | 150 |
| Solo bordes principales (limpio) | 100 | 200 |

> **Regla práctica:** `threshold2 ≈ 3 × threshold1` suele dar buenos resultados.

---

## Patrón: alternar booleano con `not`

```python
mostrar_bordes = True

if key == ord("m"):
    mostrar_bordes = not mostrar_bordes
```

`not` invierte el valor booleano en cada pulsación. Es el patrón más simple
para alternar entre dos estados (on/off, original/procesado).

---

## Por qué se necesita escala de grises antes de Canny

`cv2.Canny()` solo acepta imágenes de **1 canal**. Si se le pasa una imagen BGR
(3 canales) lanzará un error. Por eso siempre se convierte primero:

```python
gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
bordes = cv2.Canny(gris, 50, 150)
```

Y para mostrar los bordes con `imshow` junto a texto en color se convierte de vuelta:

```python
salida = cv2.cvtColor(bordes, cv2.COLOR_GRAY2BGR)
```

---

## Diferencia con programas anteriores

| Aspecto | Prog 01-05 | Prog 06 |
|---|---|---|
| Procesamiento de imagen | Mínimo | Pipeline de 3 pasos |
| Suavizado previo | No | `GaussianBlur` antes de Canny |
| Detección de bordes | No | `cv2.Canny()` |
| Alternar vista | Ciclo de lista | Booleano con `not` |

---

## Conceptos clave

- Siempre suavizar con `GaussianBlur` antes de `Canny` para eliminar ruido.
- El kernel de `GaussianBlur` debe ser de tamaño impar.
- `Canny` requiere imagen en escala de grises (1 canal).
- `threshold2 ≈ 3 × threshold1` es una buena regla de partida para los umbrales.
- La imagen de salida de `Canny` es binaria: solo blanco (borde) o negro (fondo).
