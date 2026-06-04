# Programa 13 — Trackbars para calibrar HSV

Permite ajustar rangos HSV en tiempo real usando controles deslizantes. Es una herramienta para calibrar la detección por color antes de construir detectores más completos.

Presiona `c` para cambiar preset, `m` para cambiar vista, `p` para imprimir el rango actual en la terminal y `q` para salir.

```python
import cv2

cap = cv2.VideoCapture(0)


def nada(valor):
    pass


ventana_controles = "Controles HSV"
cv2.namedWindow(ventana_controles)

cv2.createTrackbar("H min", ventana_controles, 170, 179, nada)
cv2.createTrackbar("H max", ventana_controles, 10, 179, nada)
cv2.createTrackbar("S min", ventana_controles, 80, 255, nada)
cv2.createTrackbar("S max", ventana_controles, 255, 255, nada)
cv2.createTrackbar("V min", ventana_controles, 80, 255, nada)
cv2.createTrackbar("V max", ventana_controles, 255, 255, nada)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    h_min = cv2.getTrackbarPos("H min", ventana_controles)
    h_max = cv2.getTrackbarPos("H max", ventana_controles)
    s_min = cv2.getTrackbarPos("S min", ventana_controles)
    s_max = cv2.getTrackbarPos("S max", ventana_controles)
    v_min = cv2.getTrackbarPos("V min", ventana_controles)
    v_max = cv2.getTrackbarPos("V max", ventana_controles)

    bajo = (h_min, s_min, v_min)
    alto = (h_max, s_max, v_max)
    mascara = cv2.inRange(hsv, bajo, alto)

    resultado = cv2.bitwise_and(frame, frame, mask=mascara)
    cv2.imshow("Calibracion HSV", resultado)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
```

El programa completo agrega presets, vistas y soporte para rangos circulares de matiz.

---

## Objetivo

En el programa 12 los rangos HSV estaban escritos directamente en el código:

```python
bajo = (35, 60, 60)
alto = (85, 255, 255)
```

Eso sirve para explicar la idea, pero no es cómodo para calibrar. Cada cambio exige editar el archivo, guardar y volver a ejecutar.

Este programa introduce **trackbars**, que permiten mover controles en pantalla mientras la cámara sigue funcionando.

---

## Pipeline del programa

```text
frame BGR
   │
   ▼ cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
frame HSV
   │
   ▼ leer H/S/V min y max desde trackbars
rango HSV ajustable
   │
   ▼ cv2.inRange(...)
mascara binaria
   │
   ▼ cv2.bitwise_and(...)
resultado filtrado por color
```

---

## Funciones nuevas en este programa

### `cv2.namedWindow(nombre)`

Crea una ventana con nombre.

```python
cv2.namedWindow("Controles HSV")
```

En este programa se usa para crear una ventana dedicada a los controles.

Si no se crea explícitamente, OpenCV puede crear la ventana automáticamente en algunos casos, pero para trackbars es mejor crearla antes.

---

### `cv2.createTrackbar(nombre, ventana, valor_inicial, valor_maximo, callback)`

Crea un control deslizante dentro de una ventana.

```python
cv2.createTrackbar("H min", "Controles HSV", 0, 179, nada)
```

| Parámetro | Tipo | Descripción |
|---|---|---|
| `nombre` | `str` | Nombre visible del control. |
| `ventana` | `str` | Nombre de la ventana donde se agrega. |
| `valor_inicial` | `int` | Posición inicial del control. |
| `valor_maximo` | `int` | Valor máximo permitido. |
| `callback` | función | Función que OpenCV llama cuando cambia el valor. |

La función callback recibe el nuevo valor:

```python
def nada(valor):
    pass
```

En este curso usamos una función vacía porque el loop principal lee los valores en cada frame.

---

### `cv2.getTrackbarPos(nombre, ventana)`

Lee el valor actual de un trackbar.

```python
h_min = cv2.getTrackbarPos("H min", "Controles HSV")
```

Esto permite cambiar el comportamiento del programa sin detenerlo.

El patrón completo es:

```python
h_min = cv2.getTrackbarPos("H min", ventana_controles)
h_max = cv2.getTrackbarPos("H max", ventana_controles)
s_min = cv2.getTrackbarPos("S min", ventana_controles)
s_max = cv2.getTrackbarPos("S max", ventana_controles)
v_min = cv2.getTrackbarPos("V min", ventana_controles)
v_max = cv2.getTrackbarPos("V max", ventana_controles)
```

---

### `cv2.setTrackbarPos(nombre, ventana, valor)`

Cambia la posición de un trackbar desde el código.

```python
cv2.setTrackbarPos("H min", "Controles HSV", 35)
```

El programa lo usa para aplicar presets:

```python
def aplicar_preset(nombre):
    h_min, h_max, s_min, s_max, v_min, v_max = presets[nombre]
    cv2.setTrackbarPos("H min", ventana_controles, h_min)
    cv2.setTrackbarPos("H max", ventana_controles, h_max)
```

Así se puede iniciar rápido con un color conocido y ajustar desde ahí.

---

## Trackbars del programa

| Control | Rango | Significado |
|---|---:|---|
| `H min` | `0` a `179` | Matiz mínimo |
| `H max` | `0` a `179` | Matiz máximo |
| `S min` | `0` a `255` | Saturación mínima |
| `S max` | `0` a `255` | Saturación máxima |
| `V min` | `0` a `255` | Brillo mínimo |
| `V max` | `0` a `255` | Brillo máximo |

Recuerda que OpenCV usa `H` de `0` a `179`, no de `0` a `360`.

---

## Presets incluidos

Los presets son puntos de partida:

| Preset | H min | H max | S min | S max | V min | V max |
|---|---:|---:|---:|---:|---:|---:|
| Rojo | 170 | 10 | 80 | 255 | 80 | 255 |
| Verde | 35 | 85 | 60 | 255 | 60 | 255 |
| Azul | 90 | 130 | 60 | 255 | 60 | 255 |
| Amarillo | 20 | 35 | 60 | 255 | 60 | 255 |
| Naranja | 10 | 25 | 80 | 255 | 80 | 255 |

No son valores universales. La cámara, la luz y el material del objeto pueden cambiarlos.

---

## Rango circular para el rojo

En HSV de OpenCV, el rojo aparece cerca de `0` y también cerca de `179`.

Por eso este programa interpreta lo siguiente:

```text
si H min <= H max -> rango normal
si H min > H max  -> rango circular
```

Ejemplo para rojo:

```text
H min = 170
H max = 10
```

Eso significa:

```text
H entre 170 y 179
OR
H entre 0 y 10
```

En código:

```python
mascara_1 = cv2.inRange(hsv, (170, s_min, v_min), (179, s_max, v_max))
mascara_2 = cv2.inRange(hsv, (0, s_min, v_min), (10, s_max, v_max))
mascara = cv2.bitwise_or(mascara_1, mascara_2)
```

Este detalle permite calibrar rojo sin tener que mantener dos grupos completos de trackbars.

---

## Cómo calibrar un color

1. Coloca el objeto frente a la cámara.
2. Presiona `c` hasta llegar a un preset cercano.
3. Cambia a vista `Mascara` con `m`.
4. Ajusta `H min` y `H max` hasta que el objeto quede blanco.
5. Sube `S min` para eliminar grises, blancos y zonas poco saturadas.
6. Ajusta `V min` para eliminar sombras.
7. Cambia a vista `Resultado` para validar que solo se conserva el objeto.
8. Presiona `p` para imprimir el rango final en la terminal.

---

## Qué significa cada ajuste

### `H min` y `H max`

Controlan el color permitido.

Si el objeto es verde, el rango H debe estar cerca de la zona verde. Si entra mucho fondo de otro color, reduce el rango.

---

### `S min`

Controla qué tan saturado debe ser el color.

Subir `S min` elimina:

- blancos;
- grises;
- reflejos poco coloreados;
- zonas apagadas.

Bajar `S min` permite detectar colores menos intensos, pero también puede meter ruido.

---

### `V min`

Controla qué tan brillante debe ser el píxel.

Subir `V min` elimina sombras y zonas muy oscuras. Bajarlo ayuda si el objeto está poco iluminado.

---

## Por qué se ordenan S y V

El programa permite mover libremente todos los controles. Si el usuario deja:

```text
S min = 200
S max = 50
```

ese rango no tiene sentido. Para evitar una máscara vacía, el programa ordena esos valores:

```python
s_bajo = min(s_min, s_max)
s_alto = max(s_min, s_max)
```

Con `H` no se hace eso, porque `H min > H max` tiene un significado especial: rango circular.

---

## Errores comunes

### Buscar el color en la vista Original

La vista `Original` sirve para referencia, pero para calibrar conviene usar `Mascara`.

El objetivo es que:

```text
objeto -> blanco
fondo  -> negro
```

---

### Dejar S min demasiado bajo

Si `S min` queda cerca de `0`, pueden entrar blancos, grises y reflejos.

Un valor inicial razonable suele estar entre `50` y `100`.

---

### Dejar V min demasiado alto

Si `V min` queda muy alto, el detector puede perder el objeto cuando aparece una sombra.

Un valor inicial razonable suele estar entre `50` y `100`.

---

### Usar el rango calibrado en otro ambiente sin revisarlo

Un rango calibrado con una lámpara puede fallar con luz solar o con otra cámara.

La calibración debe hacerse en condiciones parecidas a las del uso real.

---

## Ejemplos comentados

### Ejemplo 1: crear un trackbar mínimo

```python
import cv2

def nada(valor):
    pass

cv2.namedWindow("Controles")
cv2.createTrackbar("Umbral", "Controles", 127, 255, nada)
```

Comentario:

- `"Umbral"` es el nombre visible del control.
- `"Controles"` es la ventana donde aparece.
- `127` es el valor inicial.
- `255` es el valor máximo.
- `nada` es la función callback requerida por OpenCV.

Aunque la función no haga nada, OpenCV la necesita.

---

### Ejemplo 2: leer el valor del trackbar en cada frame

```python
valor = cv2.getTrackbarPos("Umbral", "Controles")
```

Comentario:

El valor se lee dentro del `while True`. Así, si el usuario mueve el control, el siguiente frame ya usa el nuevo valor.

Este patrón es la base de la calibración en vivo:

```text
mover barra -> leer valor -> recalcular máscara -> mostrar resultado
```

---

### Ejemplo 3: usar trackbars para un rango HSV normal

```python
h_min = cv2.getTrackbarPos("H min", ventana_controles)
h_max = cv2.getTrackbarPos("H max", ventana_controles)
s_min = cv2.getTrackbarPos("S min", ventana_controles)
s_max = cv2.getTrackbarPos("S max", ventana_controles)
v_min = cv2.getTrackbarPos("V min", ventana_controles)
v_max = cv2.getTrackbarPos("V max", ventana_controles)

bajo = (h_min, s_min, v_min)
alto = (h_max, s_max, v_max)

mascara = cv2.inRange(hsv, bajo, alto)
```

Comentario:

Esto funciona cuando:

```text
H min <= H max
```

Por ejemplo:

```text
verde: H min=35, H max=85
```

---

### Ejemplo 4: manejar rango circular para rojo

```python
if h_min <= h_max:
    mascara = cv2.inRange(hsv, (h_min, s_min, v_min),
                          (h_max, s_max, v_max))
else:
    mascara_1 = cv2.inRange(hsv, (h_min, s_min, v_min),
                            (179, s_max, v_max))
    mascara_2 = cv2.inRange(hsv, (0, s_min, v_min),
                            (h_max, s_max, v_max))
    mascara = cv2.bitwise_or(mascara_1, mascara_2)
```

Comentario:

Este ejemplo permite que:

```text
H min = 170
H max = 10
```

signifique:

```text
170..179 OR 0..10
```

Es una forma compacta de calibrar rojo con un solo par de trackbars `H min` y `H max`.

---

### Ejemplo 5: copiar valores calibrados a otro programa

Cuando presionas `p`, el programa imprime algo como:

```text
Valores: h_min=42, h_max=78, s_min=80, s_max=255, v_min=60, v_max=255
```

Luego puedes usarlo como rango fijo:

```python
bajo = (42, 80, 60)
alto = (78, 255, 255)
mascara = cv2.inRange(hsv, bajo, alto)
```

Comentario:

Este es el flujo recomendado:

```text
programa 13 -> calibrar valores
programa 12/14/15 -> usar valores ya calibrados
```

---

### Ejemplo 6: detectar si la calibración está demasiado abierta

```python
pixeles = cv2.countNonZero(mascara)
total = mascara.shape[0] * mascara.shape[1]
porcentaje = (pixeles / total) * 100

if porcentaje > 40:
    print("El rango probablemente esta detectando demasiado fondo")
```

Comentario:

Si la máscara ocupa casi toda la imagen, normalmente conviene:

- subir `S min`;
- subir `V min` si hay sombras;
- reducir el rango entre `H min` y `H max`.

---

## Diferencia con programas anteriores

| Programa | Qué hacía | Qué aporta este programa |
|---|---|---|
| Programa 12 | Usaba rangos HSV escritos en código | Permite ajustar los rangos en tiempo real |
| Programa 11 | Creaba máscaras por intensidad | Crea máscaras por color con control interactivo |
| Programa 05 | Mostraba HSV como espacio de color | Usa HSV como herramienta práctica de segmentación |

---

## Relación con los siguientes programas

Los valores calibrados aquí se reutilizarán en detectores posteriores.

Después de calibrar color, el flujo natural es:

```text
mascara HSV
  -> limpieza morfológica
  -> contornos
  -> cajas delimitadoras
  -> detector por color y forma
```

El siguiente programa será morfología o una preparación hacia ella: limpiar ruido, cerrar huecos y mejorar la máscara antes de buscar contornos.

---

## Conceptos clave

- Una trackbar permite modificar parámetros mientras el programa está corriendo.
- `cv2.createTrackbar` crea el control.
- `cv2.getTrackbarPos` lee el valor actual.
- `cv2.setTrackbarPos` permite aplicar presets desde el código.
- En OpenCV, `H` va de `0` a `179`.
- Para rojo conviene usar rango circular.
- La calibración HSV depende de luz, cámara y objeto.
