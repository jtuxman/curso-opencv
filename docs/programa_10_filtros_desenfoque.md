# Programa 10 — Filtros de desenfoque

Permite comparar en tiempo real tres tipos de desenfoque: gaussiano, mediano y bilateral. Presiona `m` para ciclar entre los filtros, `q` para salir.

```python
import cv2

cap = cv2.VideoCapture(0)

filtros = ["Sin filtro", "Gaussiano", "Mediano", "Bilateral"]
indice  = 0

while True:
    ret, frame = cap.read()

    if not ret:
        break

    filtro = filtros[indice]

    if filtro == "Gaussiano":
        salida = cv2.GaussianBlur(frame, (15, 15), 0)
    elif filtro == "Mediano":
        salida = cv2.medianBlur(frame, 15)
    elif filtro == "Bilateral":
        salida = cv2.bilateralFilter(frame, 9, 75, 75)
    else:
        salida = frame

    cv2.putText(salida, f"Filtro: {filtro}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("Filtros de desenfoque", salida)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("m"):
        indice = (indice + 1) % len(filtros)
    elif key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
```

---

## Concepto: ¿para qué sirve el desenfoque?

El desenfoque no es solo un efecto visual — tiene usos prácticos en visión por computadora:

| Uso | Filtro recomendado |
|---|---|
| Eliminar ruido antes de Canny (prog 06) | Gaussiano |
| Eliminar ruido tipo sal y pimienta | Mediano |
| Suavizar preservando bordes (piel, segmentación) | Bilateral |
| Velocidad máxima en tiempo real | Gaussiano |

---

## Funciones nuevas en este programa

### `cv2.GaussianBlur(src, ksize, sigmaX)` *(repaso)*

Ya vista en el programa 06, ahora se aplica sobre el frame BGR completo en lugar
de solo sobre la imagen en gris.

```python
suave = cv2.GaussianBlur(frame, (15, 15), 0)
```

Cuanto mayor el kernel, mayor el desenfoque. Siempre debe ser impar: 3, 5, 7, 15...

---

### `cv2.medianBlur(src, ksize)`

Reemplaza cada píxel por la **mediana** de sus vecinos dentro del kernel.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `src` | `ndarray` | Imagen de entrada (funciona con 1 o 3 canales). |
| `ksize` | `int` | Tamaño del kernel. Debe ser impar y positivo. |

**Retorna:** `ndarray` — imagen filtrada.

```python
salida = cv2.medianBlur(frame, 5)    # kernel 5x5
salida = cv2.medianBlur(frame, 15)   # más suave
```

#### Cómo funciona la mediana

Para cada píxel, toma todos los valores en su vecindad (ej. 5×5 = 25 píxeles),
los ordena y elige el del centro (la mediana).

```
Vecindad 3x3:   [10, 20, 200, 15, 18, 22, 19, 17, 21]
Ordenados:      [10, 15, 17, 18, 19, 20, 21, 22, 200]
Mediana:        19   ← el 200 (ruido) queda eliminado
```

> **Ventaja sobre Gaussiano:** el filtro mediano elimina valores extremos
> (píxeles blancos o negros aislados = ruido *sal y pimienta*) sin que esos
> valores afecten el resultado, ya que la mediana ignora los extremos.

---

### `cv2.bilateralFilter(src, d, sigmaColor, sigmaSpace)`

Desenfoca la imagen pero **preserva los bordes**. Es más lento que los otros
dos pero produce resultados de mayor calidad visual.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `src` | `ndarray` | Imagen de entrada (solo 8-bit o float). |
| `d` | `int` | Diámetro del vecindario de cada píxel. `-1` lo calcula desde `sigmaSpace`. |
| `sigmaColor` | `float` | Rango de colores a mezclar. Mayor valor = mezcla colores más distintos. |
| `sigmaSpace` | `float` | Influencia de píxeles lejanos. Mayor valor = área de influencia más grande. |

**Retorna:** `ndarray` — imagen filtrada con bordes preservados.

```python
salida = cv2.bilateralFilter(frame, 9, 75, 75)   # balance general
salida = cv2.bilateralFilter(frame, 9, 150, 150) # más suavizado
```

#### Cómo funciona (concepto)

Un filtro gaussiano trata igual a todos los píxeles vecinos. El bilateral
aplica **dos pesos**:

1. **Peso espacial** (`sigmaSpace`): píxeles más cercanos influyen más (igual que gaussiano).
2. **Peso de color** (`sigmaColor`): píxeles con color similar influyen más; píxeles
   muy distintos (bordes) influyen poco.

El resultado: zonas uniformes se suavizan, pero los bordes donde hay un cambio
brusco de color se conservan nítidos.

#### Guía de valores

| Objetivo | d | sigmaColor | sigmaSpace |
|---|---|---|---|
| Tiempo real (rápido) | 5 | 50 | 50 |
| Balance general | 9 | 75 | 75 |
| Máximo suavizado | 15 | 150 | 150 |

> **Rendimiento:** `bilateralFilter` es significativamente más lento que
> `GaussianBlur` y `medianBlur`. Con `d=9` es usable en tiempo real;
> valores mayores pueden bajar el FPS notablemente.

---

## Comparación de los tres filtros

| Característica | Gaussiano | Mediano | Bilateral |
|---|---|---|---|
| Velocidad | Muy rápido | Rápido | Lento |
| Elimina ruido general | Sí | Sí | Sí |
| Elimina ruido sal/pimienta | Regular | Muy bien | Regular |
| Preserva bordes | No | Parcialmente | Sí |
| Uso típico | Pre-procesado general | Ruido puntual | Efectos visuales, piel |

---

## Diferencia con programas anteriores

| Aspecto | Prog 06 (bordes) | Prog 10 (desenfoque) |
|---|---|---|
| `GaussianBlur` | Solo en gris, pre-proceso | En color, como efecto final |
| Filtros nuevos | — | `medianBlur`, `bilateralFilter` |
| Propósito | Reducir ruido antes de Canny | Comparar efectos visuales |

---

## Conceptos clave

- `GaussianBlur`: rápido, uso general, para pre-procesado.
- `medianBlur`: ideal para ruido tipo sal y pimienta (píxeles aislados muy claros u oscuros).
- `bilateralFilter`: más lento, preserva bordes — útil para suavizar piel o segmentación.
- Los tres kernels deben ser de tamaño impar.
- En tiempo real preferir `GaussianBlur`; `bilateralFilter` con `d` pequeño si se necesita preservar bordes.
