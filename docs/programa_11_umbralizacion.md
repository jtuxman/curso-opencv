# Programa 11 — Umbralización

Compara en tiempo real varios métodos de umbralización: binaria, binaria invertida, adaptativa y Otsu. Presiona `m` para cambiar de modo, `+` o `-` para ajustar el umbral manual, y `q` para salir.

```python
import cv2

cap = cv2.VideoCapture(0)

modos = [
    "Original",
    "Gris",
    "Binaria",
    "Binaria invertida",
    "Adaptativa media",
    "Adaptativa gaussiana",
    "Otsu",
]

indice = 0
umbral = 127
valor_maximo = 255
block_size = 11
constante_c = 2

while True:
    ret, frame = cap.read()

    if not ret:
        break

    modo = modos[indice]
    gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if modo == "Binaria":
        _, mascara = cv2.threshold(gris, umbral, valor_maximo, cv2.THRESH_BINARY)
        salida = cv2.cvtColor(mascara, cv2.COLOR_GRAY2BGR)
    elif modo == "Binaria invertida":
        _, mascara = cv2.threshold(gris, umbral, valor_maximo, cv2.THRESH_BINARY_INV)
        salida = cv2.cvtColor(mascara, cv2.COLOR_GRAY2BGR)
    elif modo == "Adaptativa media":
        mascara = cv2.adaptiveThreshold(
            gris, valor_maximo, cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY, block_size, constante_c
        )
        salida = cv2.cvtColor(mascara, cv2.COLOR_GRAY2BGR)
    elif modo == "Adaptativa gaussiana":
        mascara = cv2.adaptiveThreshold(
            gris, valor_maximo, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, block_size, constante_c
        )
        salida = cv2.cvtColor(mascara, cv2.COLOR_GRAY2BGR)
    elif modo == "Otsu":
        gris_suave = cv2.GaussianBlur(gris, (5, 5), 0)
        _, mascara = cv2.threshold(
            gris_suave, 0, valor_maximo, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )
        salida = cv2.cvtColor(mascara, cv2.COLOR_GRAY2BGR)
    elif modo == "Gris":
        salida = cv2.cvtColor(gris, cv2.COLOR_GRAY2BGR)
    else:
        salida = frame

    cv2.imshow("Umbralizacion", salida)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("m"):
        indice = (indice + 1) % len(modos)
    elif key == ord("+"):
        umbral = min(255, umbral + 5)
    elif key == ord("-"):
        umbral = max(0, umbral - 5)
    elif key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
```

---

## Concepto: ¿qué es umbralizar?

Umbralizar significa convertir una imagen en una decisión por píxel. Cada píxel se clasifica como:

| Valor | Significado visual | Uso típico |
|---|---|---|
| `255` | Blanco | Objeto, región seleccionada, primer plano |
| `0` | Negro | Fondo, región descartada |

El resultado se llama **máscara binaria**.

```
Imagen en gris:
[ 20][ 35][ 80][130][180][230]

Umbral = 127

Máscara binaria:
[  0][  0][  0][255][255][255]
```

La umbralización es importante porque muchos pasos posteriores trabajan mejor con imágenes binarias:

- encontrar contornos;
- medir áreas;
- detectar movimiento;
- separar objetos del fondo;
- crear regiones de interés.

---

## Pipeline del programa

```
frame BGR
   │
   ▼ cv2.cvtColor(COLOR_BGR2GRAY)
gris
   │
   ├── cv2.threshold(...)
   │       └── máscara binaria con umbral manual
   │
   ├── cv2.adaptiveThreshold(...)
   │       └── máscara con umbral local por zonas
   │
   └── cv2.threshold(... + THRESH_OTSU)
           └── máscara con umbral global calculado automáticamente
```

---

## Por qué se convierte a escala de grises

Una imagen BGR tiene tres canales:

```python
frame.shape  # (alto, ancho, 3)
```

Cada píxel tiene tres valores:

```python
[B, G, R]
```

La umbralización básica necesita comparar un solo número por píxel. Por eso se convierte primero a escala de grises:

```python
gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
```

Ahora cada píxel representa intensidad:

```python
gris.shape  # (alto, ancho)
```

Valores bajos son oscuros; valores altos son claros.

---

## Funciones nuevas en este programa

### `cv2.threshold(src, thresh, maxval, type)`

Aplica un umbral global. Global significa que el mismo valor de umbral se usa en toda la imagen.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `src` | `ndarray` | Imagen de entrada. Normalmente escala de grises. |
| `thresh` | `float` | Valor de corte. En este programa empieza en `127`. |
| `maxval` | `float` | Valor asignado a los píxeles que cumplen la condición. Normalmente `255`. |
| `type` | `int` | Tipo de umbralización: binaria, invertida, truncada, Otsu, etc. |

**Retorna:** tupla `(ret, dst)`

| Retorno | Descripción |
|---|---|
| `ret` | Umbral usado. En umbral manual coincide con `thresh`; con Otsu es el valor calculado. |
| `dst` | Imagen resultante. En este programa es una máscara de `0` y `255`. |

**Ejemplo básico:**

```python
ret, mascara = cv2.threshold(gris, 127, 255, cv2.THRESH_BINARY)
```

Si un píxel vale `180`:

```python
180 > 127  # True -> se vuelve 255
```

Si un píxel vale `80`:

```python
80 > 127   # False -> se vuelve 0
```

---

### `cv2.THRESH_BINARY`

Convierte en blanco los píxeles mayores al umbral.

```python
_, mascara = cv2.threshold(gris, 127, 255, cv2.THRESH_BINARY)
```

Regla:

```text
si pixel > umbral  -> 255
si pixel <= umbral -> 0
```

Uso típico: objeto claro sobre fondo oscuro.

---

### `cv2.THRESH_BINARY_INV`

Es la versión invertida.

```python
_, mascara = cv2.threshold(gris, 127, 255, cv2.THRESH_BINARY_INV)
```

Regla:

```text
si pixel > umbral  -> 0
si pixel <= umbral -> 255
```

Uso típico: objeto oscuro sobre fondo claro.

---

### `cv2.adaptiveThreshold(src, maxValue, adaptiveMethod, thresholdType, blockSize, C)`

Calcula un umbral diferente para cada zona de la imagen. Es útil cuando la iluminación no es uniforme.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `src` | `ndarray` | Imagen de entrada en escala de grises. |
| `maxValue` | `float` | Valor asignado a los píxeles seleccionados. Normalmente `255`. |
| `adaptiveMethod` | `int` | Método para calcular el umbral local. |
| `thresholdType` | `int` | Normalmente `cv2.THRESH_BINARY` o `cv2.THRESH_BINARY_INV`. |
| `blockSize` | `int` | Tamaño de la vecindad local. Debe ser impar y mayor que 1. |
| `C` | `float` | Constante que se resta al promedio local. |

**Retorna:** imagen binaria.

Ejemplo:

```python
mascara = cv2.adaptiveThreshold(
    gris,
    255,
    cv2.ADAPTIVE_THRESH_MEAN_C,
    cv2.THRESH_BINARY,
    11,
    2,
)
```

La idea general es:

```text
umbral_local = promedio_de_la_vecindad - C
```

Cada píxel se compara contra el umbral de su propia zona, no contra un valor global.

---

### `cv2.ADAPTIVE_THRESH_MEAN_C`

Usa el promedio simple de la vecindad local.

```python
mascara = cv2.adaptiveThreshold(
    gris, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
    cv2.THRESH_BINARY, 11, 2
)
```

Es rápido y fácil de interpretar, pero puede ser sensible al ruido.

---

### `cv2.ADAPTIVE_THRESH_GAUSSIAN_C`

Usa un promedio ponderado. Los píxeles cercanos al centro pesan más que los lejanos.

```python
mascara = cv2.adaptiveThreshold(
    gris, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY, 11, 2
)
```

Suele funcionar mejor cuando hay sombras suaves o cambios graduales de luz.

---

### `cv2.THRESH_OTSU`

Otsu calcula automáticamente el umbral global. No se le da un umbral manual útil; se pasa `0` y OpenCV encuentra el valor.

```python
umbral_otsu, mascara = cv2.threshold(
    gris, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
)
```

En este caso:

```python
umbral_otsu
```

contiene el valor elegido por el algoritmo.

Otsu funciona mejor cuando la imagen tiene dos grupos claros de intensidad:

- fondo oscuro y objeto claro;
- fondo claro y objeto oscuro;
- documento con letras oscuras sobre papel claro.

Funciona peor cuando hay muchos tonos mezclados o iluminación muy irregular.

---

## Por qué se suaviza antes de Otsu

El programa usa:

```python
gris_suave = cv2.GaussianBlur(gris, (5, 5), 0)
```

antes de aplicar Otsu.

Esto reduce ruido pequeño de la cámara. Sin suavizado, píxeles aislados muy claros u oscuros pueden alterar el histograma y hacer que el umbral calculado sea menos estable.

---

## Comparación de métodos

| Método | Ventaja | Desventaja | Cuándo usarlo |
|---|---|---|---|
| Binaria | Simple y rápida | Falla con iluminación irregular | Objeto claro sobre fondo oscuro |
| Binaria invertida | Simple y rápida | Falla con iluminación irregular | Objeto oscuro sobre fondo claro |
| Adaptativa media | Se adapta por zonas | Puede generar ruido local | Documentos o escenas con sombras |
| Adaptativa gaussiana | Mejor ante cambios suaves de luz | Más costosa que media | Iluminación desigual |
| Otsu | Elige el umbral automáticamente | Requiere grupos de intensidad separables | Fondos simples, documentos, objetos contrastados |

---

## Efecto de subir o bajar el umbral

En los modos binarios manuales, el programa permite cambiar el umbral con `+` y `-`.

```python
umbral = min(255, umbral + 5)
umbral = max(0, umbral - 5)
```

Si subes el umbral:

- menos píxeles superan la condición;
- la máscara blanca se reduce;
- solo quedan zonas más claras.

Si bajas el umbral:

- más píxeles superan la condición;
- la máscara blanca crece;
- zonas medianamente claras también se seleccionan.

---

## Errores comunes

### Usar BGR directamente en `threshold`

```python
_, mascara = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY)
```

No es lo recomendado para este curso porque `frame` tiene tres canales. Convierte primero a gris:

```python
gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
_, mascara = cv2.threshold(gris, 127, 255, cv2.THRESH_BINARY)
```

---

### Confundir objeto blanco con fondo blanco

OpenCV suele trabajar mejor si el objeto de interés queda blanco y el fondo negro, especialmente antes de encontrar contornos.

Si tu objeto queda negro y el fondo blanco, prueba:

```python
cv2.THRESH_BINARY_INV
```

---

### Usar `blockSize` par en umbralización adaptativa

Esto es incorrecto:

```python
cv2.adaptiveThreshold(gris, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                      cv2.THRESH_BINARY, 10, 2)
```

`blockSize` debe ser impar:

```python
cv2.adaptiveThreshold(gris, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                      cv2.THRESH_BINARY, 11, 2)
```

---

### Esperar que Otsu siempre sea perfecto

Otsu no entiende objetos. Solo analiza intensidades. Si el fondo y el objeto tienen tonos parecidos, o si hay muchas sombras, puede elegir un umbral poco útil.

En esos casos se puede probar:

- mejorar iluminación;
- usar umbral adaptativo;
- segmentar por color en HSV;
- aplicar morfología para limpiar ruido.

---

## Diferencia con programas anteriores

| Programa | Qué hacía | Qué aporta este programa |
|---|---|---|
| Programa 05 | Convertía espacios de color | Usa escala de grises como entrada para tomar decisiones por píxel |
| Programa 06 | Detectaba bordes | Produce máscaras llenas, no solo líneas de borde |
| Programa 10 | Aplicaba filtros | Usa suavizado como preparación para una decisión binaria |

---

## Relación con los siguientes programas

La umbralización prepara la base para:

- `programa_12_segmentacion_por_color_hsv.py`: separar objetos usando color;
- `programa_14_morfologia.py`: limpiar máscaras binarias;
- `programa_15_contornos_y_bounding_boxes.py`: encontrar regiones y medirlas.

El flujo típico será:

```text
frame
  -> conversión / filtro
  -> máscara binaria
  -> limpieza morfológica
  -> contornos
  -> cajas y mediciones
```

---

## Conceptos clave

- Una máscara binaria tiene valores `0` y `255`.
- El objeto de interés normalmente debe quedar blanco.
- `cv2.threshold` usa un umbral global.
- `cv2.adaptiveThreshold` usa umbrales locales.
- Otsu calcula automáticamente un umbral global.
- La iluminación afecta directamente la calidad de una máscara.
- Las máscaras serán la entrada natural para morfología y contornos.
