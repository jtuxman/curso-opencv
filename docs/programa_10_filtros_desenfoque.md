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

El desenfoque no es solo un efecto visual — tiene usos importantes en visión por computadora:

| Uso | Descripción | Filtro recomendado |
|---|---|---|
| Eliminar ruido antes de Canny | Suavizar antes de detectar bordes (prog. 06) | Gaussiano |
| Eliminar ruido sal y pimienta | Píxeles blancos/negros aislados | Mediano |
| Suavizar preservando contornos | Difuminar sin perder bordes | Bilateral |
| Efecto de privacidad | Censurar rostros o textos | Gaussiano con kernel grande |

---

## Funciones en este programa

### `cv2.GaussianBlur(src, ksize, sigmaX)` *(repaso de prog. 06)*

Aplica desenfoque gaussiano. Cada píxel se reemplaza por el **promedio ponderado** de sus vecinos (píxeles más cercanos tienen más peso).

| Parámetro | Tipo | Descripción |
|---|---|---|
| `src` | `ndarray` | Imagen de entrada (1 o 3 canales). |
| `ksize` | `tuple (w, h)` | Tamaño del kernel. Debe ser impar: 3, 5, 7, 9... |
| `sigmaX` | `float` | Desviación estándar. `0` = calculada automáticamente. |

**Ejemplos:**

```python
# Niveles de desenfoque (kernel mayor = más borroso):
leve   = cv2.GaussianBlur(frame, (3, 3), 0)    # apenas perceptible
medio  = cv2.GaussianBlur(frame, (15, 15), 0)  # este programa
fuerte = cv2.GaussianBlur(frame, (31, 31), 0)  # muy borroso
extremo = cv2.GaussianBlur(frame, (51, 51), 0) # efecto privacidad

# Censurar una región del frame (efecto privacidad/mosaico):
y1, y2, x1, x2 = 100, 200, 150, 300           # coordenadas de la región
region = frame[y1:y2, x1:x2]                  # recortar la región
censurada = cv2.GaussianBlur(region, (51, 51), 0)  # difuminar fuertemente
frame[y1:y2, x1:x2] = censurada               # reemplazar en el frame

# Aplicar antes de Canny para reducir falsos bordes:
gris    = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
suave   = cv2.GaussianBlur(gris, (5, 5), 0)
bordes  = cv2.Canny(suave, 50, 150)
```

---

### `cv2.medianBlur(src, ksize)`

Reemplaza cada píxel por la **mediana** (valor del centro al ordenar) de sus vecinos. Elimina eficazmente el ruido tipo "sal y pimienta".

| Parámetro | Tipo | Descripción |
|---|---|---|
| `src` | `ndarray` | Imagen de entrada (1 o 3 canales). |
| `ksize` | `int` | Tamaño del kernel cuadrado. Debe ser impar y mayor que 1. |

**Retorna:** `ndarray` — imagen filtrada. No modifica la original.

**Cómo funciona la mediana:**

```
Vecindad 3x3 de un píxel (9 valores):
[10][20][200]
[15][18][22 ]   → ordenados: [10, 15, 17, 18, 19, 20, 21, 22, 200]
[19][17][21 ]   → mediana (posición central): 19

El valor 200 (ruido blanco) no afecta el resultado.
Un promedio daría: (10+15+200+...) / 9 = 38 ← contaminado por el ruido
La mediana da: 19 ← valor representativo sin contaminación
```

**Ejemplos:**

```python
# Diferentes tamaños de kernel:
suave3  = cv2.medianBlur(frame, 3)    # kernel 3x3, suave
suave7  = cv2.medianBlur(frame, 7)    # kernel 7x7, más agresivo
suave15 = cv2.medianBlur(frame, 15)   # este programa

# Caso de uso: limpiar una imagen con ruido sal y pimienta:
# (simular ruido para ver el efecto)
import numpy as np
frame_ruidoso = frame.copy()
# agregar píxeles blancos y negros aleatorios:
ruido = np.random.randint(0, 2, frame.shape[:2])
frame_ruidoso[ruido == 0] = 0    # píxeles negros (sal)
frame_ruidoso[ruido == 1] = 255  # píxeles blancos (pimienta)

limpio = cv2.medianBlur(frame_ruidoso, 5)   # elimina el ruido eficazmente

# Comparación visual:
cv2.imshow("Con ruido", frame_ruidoso)
cv2.imshow("Limpio",    limpio)
```

---

### `cv2.bilateralFilter(src, d, sigmaColor, sigmaSpace)`

Desenfoca la imagen **preservando los bordes**. Es más lento que los anteriores pero produce mejor resultado visual porque no mezcla colores muy distintos entre sí.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `src` | `ndarray` | Imagen de entrada (solo `uint8` o `float32`). |
| `d` | `int` | Diámetro del vecindario. `-1` lo calcula desde `sigmaSpace`. |
| `sigmaColor` | `float` | Rango de colores a mezclar. Mayor = mezcla colores más distintos. |
| `sigmaSpace` | `float` | Influencia espacial. Mayor = toma en cuenta píxeles más lejanos. |

**Retorna:** `ndarray` — imagen filtrada con bordes preservados. No modifica la original.

**Cómo funciona (concepto):**

Un filtro gaussiano aplica un solo peso (distancia espacial). El bilateral aplica **dos pesos simultáneos**:

```
Peso del píxel vecino = peso_espacial × peso_color

peso_espacial: píxeles más cercanos tienen mayor influencia
               (igual que en gaussiano)

peso_color:    píxeles con color SIMILAR tienen mayor influencia
               píxeles con color MUY DIFERENTE tienen influencia casi nula
               → los bordes (cambio brusco de color) no se suavizan
```

```
Zona uniforme (pared):         Borde (pared → persona):
[200][198][201][199]           [200][199][80][82]
    ↑ colores similares             ↑ cambio brusco
    → se mezclan con peso alto      → peso bajo, NO se mezclan
    → zona suavizada                → borde preservado
```

**Ejemplos:**

```python
# Diferentes niveles de bilateralFilter:
suave   = cv2.bilateralFilter(frame, 5,  50,  50)   # tiempo real, poco efecto
balance = cv2.bilateralFilter(frame, 9,  75,  75)   # este programa
fuerte  = cv2.bilateralFilter(frame, 9,  150, 150)  # más suavizado, más lento
extremo = cv2.bilateralFilter(frame, 15, 200, 200)  # muy lento, muy suave

# Efecto "filtro de belleza" (suavizar piel preservando ojos/boca):
suavizado = cv2.bilateralFilter(frame, 9, 75, 75)
cv2.imshow("Efecto suavizado", suavizado)

# Guía de valores:
# d=5,  sigma=50  → rápido, efecto sutil
# d=9,  sigma=75  → balance rendimiento/calidad
# d=15, sigma=150 → lento, efecto pronunciado

# ADVERTENCIA: d > 9 puede bajar el FPS notablemente en tiempo real
```

---

## Comparación de los tres filtros

| Característica | Gaussiano | Mediano | Bilateral |
|---|---|---|---|
| Velocidad | Muy rápido | Rápido | Lento |
| Suaviza zonas uniformes | Sí | Sí | Sí |
| Elimina ruido aleatorio | Sí | Sí | Sí |
| Elimina ruido sal/pimienta | Parcial | Excelente | Parcial |
| Preserva bordes | No — los suaviza | Parcialmente | Sí — los mantiene nítidos |
| Uso típico | Pre-procesado, privacidad | Imágenes con ruido puntual | Suavizar piel, segmentación |
| Kernel válido | Impar: 3, 5, 7... | Impar: 3, 5, 7... | `d` cualquier entero |

### Visualización del efecto en bordes

```
Imagen original:
[10][10][10][10][200][200][200][200]
                  ↑ borde

Gaussiano (kernel 5):
[10][10][15][82][128][185][200][200]   ← borde difuminado (se "esparce")

Mediano (kernel 5):
[10][10][10][10][200][200][200][200]   ← borde preservado

Bilateral (d=9):
[10][10][10][10][200][200][200][200]   ← borde preservado + zonas suavizadas
```

---

## Diferencia con prog. 06 (donde también aparece GaussianBlur)

| Aspecto | Prog. 06 | Prog. 10 |
|---|---|---|
| Propósito del blur | Pre-procesado para reducir falsos bordes en Canny | Efecto visual final |
| Canal de entrada | Gris (1 canal) | BGR color (3 canales) |
| Tamaño del kernel | Pequeño `(5,5)` — solo eliminar ruido | Grande `(15,15)` — efecto visible |
| Resultado | Se descarta, solo sirve para Canny | Se muestra en pantalla |

---

## Conceptos clave

- `GaussianBlur`: rápido, para pre-procesado y privacidad.
- `medianBlur`: ideal para ruido tipo sal y pimienta (píxeles aislados blancos/negros).
- `bilateralFilter`: más lento, el único que preserva los bordes correctamente.
- Los tres kernels deben ser de tamaño impar.
- Para tiempo real preferir Gaussiano; bilateralFilter con `d` pequeño si se necesita preservar bordes.
