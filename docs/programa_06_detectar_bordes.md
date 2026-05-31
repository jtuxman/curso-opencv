# Programa 06 — Detección de bordes con Canny

Detecta bordes en tiempo real usando el algoritmo Canny. Presiona `m` para alternar entre la imagen original y los bordes. Presiona `q` para salir.

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

Un **borde** en una imagen es una zona donde la intensidad de los píxeles cambia bruscamente. Por ejemplo, el límite entre un objeto oscuro y un fondo claro.

```
Fondo claro (200) → borde → Objeto oscuro (30)
[200][200][200][150][80][30][30][30]
                 ↑ borde aquí (cambio brusco)
```

Matemáticamente, un borde es donde la **derivada** (gradiente) de la intensidad es alta.

---

## Pipeline de detección (3 pasos)

```
frame (BGR, 3 canales)
       │
       ▼ cv2.cvtColor(COLOR_BGR2GRAY)
gris (1 canal) — necesario porque Canny requiere 1 canal
       │
       ▼ cv2.GaussianBlur((5,5), 0)
gris suavizado — elimina ruido que generaría falsos bordes
       │
       ▼ cv2.Canny(umbral1, umbral2)
bordes (binario: 255=borde, 0=fondo)
```

---

## Funciones nuevas en este programa

### `cv2.GaussianBlur(src, ksize, sigmaX)`

Aplica un desenfoque gaussiano para reducir el ruido antes de detectar bordes.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `src` | `ndarray` | Imagen de entrada (1 o 3 canales). |
| `ksize` | `tuple (w, h)` | Tamaño del kernel. Ambos valores deben ser **impares y positivos**. |
| `sigmaX` | `float` | Desviación estándar en X. `0` = calculada automáticamente desde `ksize`. |

**Retorna:** `ndarray` — imagen suavizada. No modifica la original.

**Ejemplos:**

```python
# Diferentes niveles de suavizado:
suave3  = cv2.GaussianBlur(gris, (3, 3), 0)    # suave, casi sin efecto
suave5  = cv2.GaussianBlur(gris, (5, 5), 0)    # balance para tiempo real
suave11 = cv2.GaussianBlur(gris, (11, 11), 0)  # muy suave, menos bordes falsos
suave21 = cv2.GaussianBlur(gris, (21, 21), 0)  # extremo, solo bordes principales

# Kernel asimétrico (poco común pero válido):
cv2.GaussianBlur(gris, (5, 3), 0)   # más suavizado horizontal que vertical

# Con sigma explícito (mayor sigma = más desenfoque):
cv2.GaussianBlur(gris, (0, 0), sigmaX=2.0)   # sigma define el área de influencia

# El kernel DEBE ser impar:
# cv2.GaussianBlur(gris, (4, 4), 0)  ← ERROR: 4 es par
# cv2.GaussianBlur(gris, (5, 5), 0)  ← CORRECTO
```

> **¿Por qué es necesario antes de Canny?**
> La cámara introduce ruido aleatorio en cada frame (pequeñas variaciones de brillo
> píxel a píxel). Sin suavizar, Canny detecta esas variaciones como "cambios bruscos"
> y genera cientos de bordes falsos en zonas uniformes. El GaussianBlur los elimina.

---

### `cv2.Canny(image, threshold1, threshold2)`

Detecta bordes usando el algoritmo de John Canny (1986). Es el detector de bordes más usado en visión por computadora.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `image` | `ndarray` | Imagen en **escala de grises** (1 canal). Pasa error si recibe BGR. |
| `threshold1` | `float` | Umbral inferior para el criterio de histéresis. |
| `threshold2` | `float` | Umbral superior para el criterio de histéresis. |

**Retorna:** `ndarray` — imagen binaria: `255` (blanco) = borde, `0` (negro) = fondo.

**Ejemplos:**

```python
# Configuraciones para diferentes situaciones:

# Muchos bordes (sensible, captura detalles finos):
bordes = cv2.Canny(gris, 20, 60)

# Balance general (el más usado):
bordes = cv2.Canny(gris, 50, 150)

# Pocos bordes (solo los más marcados, imagen más limpia):
bordes = cv2.Canny(gris, 100, 200)

# Regla práctica: threshold2 ≈ 3 × threshold1
# threshold1=30  → threshold2=90
# threshold1=50  → threshold2=150
# threshold1=100 → threshold2=300

# Canny requiere imagen de 1 canal:
bordes = cv2.Canny(gris, 50, 150)    # CORRECTO: gris tiene 1 canal
# bordes = cv2.Canny(frame, 50, 150) # ERROR: frame tiene 3 canales BGR

# Usar la imagen de bordes para contar o analizar contornos:
contornos, _ = cv2.findContours(bordes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print(f"Contornos detectados: {len(contornos)}")
```

#### Cómo funcionan los umbrales (histéresis)

El algoritmo clasifica cada píxel según su gradiente (magnitud del cambio de intensidad):

```
Gradiente del píxel:
  0 ──── threshold1 ──────────── threshold2 ──►
  │           │                       │
descarte    borde débil           borde fuerte
(siempre)   (solo si conecta       (siempre
             con borde fuerte)      incluido)
```

Ejemplo con umbral1=50, umbral2=150:

```
Gradiente=200 → borde fuerte → incluido siempre ✓
Gradiente=80  → borde débil  → incluido si toca un borde fuerte ✓/✗
Gradiente=30  → descartado   → nunca incluido ✗
```

Este sistema de dos umbrales reduce los bordes ruidosos sin perder los importantes.

---

## Patrón: alternar booleano con `not`

```python
mostrar_bordes = True

if key == ord("m"):
    mostrar_bordes = not mostrar_bordes
# True  → False → True → False → ...
```

`not` invierte el valor booleano en cada pulsación. Patrón más simple para toggle on/off.

```python
# Comparación de patrones para alternar estados:

# Patrón con not (2 estados):
activo = not activo

# Patrón con lista y % (N estados):
modos = ["A", "B", "C"]
indice = (indice + 1) % len(modos)

# Usar not cuando hay solo 2 opciones; lista+% cuando hay 3 o más.
```

---

## Diferencia con programas anteriores

| Aspecto | Prog 01-05 | Prog 06 |
|---|---|---|
| Procesamiento | Mínimo o conversión simple | Pipeline de 3 pasos |
| Suavizado previo | No | `GaussianBlur` obligatorio antes de Canny |
| Detección de bordes | No | `cv2.Canny()` |
| Alternar vista | Ciclo de lista | Booleano con `not` |

---

## Conceptos clave

- Siempre suavizar con `GaussianBlur` antes de `Canny` — sin esto el ruido genera falsos bordes.
- El kernel de `GaussianBlur` debe ser de tamaño **impar**.
- `Canny` requiere imagen en escala de grises (1 canal); pasar BGR causa error.
- `threshold2 ≈ 3 × threshold1` es una buena regla de partida.
- La salida de `Canny` es binaria: solo `0` (fondo) o `255` (borde).
- Convertir la salida de Canny a BGR con `COLOR_GRAY2BGR` antes de dibujar texto en color.
