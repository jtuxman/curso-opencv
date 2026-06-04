# Programa 14 — Morfologia

Aplica operaciones morfologicas sobre una mascara binaria generada por segmentacion HSV. Permite comparar la mascara original contra la mascara procesada antes de pasar a contornos.

Presiona `m` para cambiar operacion, `v` para cambiar vista, `c` para cambiar color, `+` o `-` para ajustar el kernel, `i` para cambiar iteraciones y `q` para salir.

```python
import cv2

cap = cv2.VideoCapture(0)

operaciones = [
    "Sin morfologia",
    "Erosion",
    "Dilatacion",
    "Apertura",
    "Cierre",
]

tamanios_kernel = [3, 5, 7, 9, 11, 15]
indice_kernel = 1
iteraciones = 1

while True:
    ret, frame = cap.read()

    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mascara_original = cv2.inRange(hsv, (35, 60, 60), (85, 255, 255))

    tamanio_kernel = tamanios_kernel[indice_kernel]
    kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT, (tamanio_kernel, tamanio_kernel)
    )

    mascara_procesada = cv2.morphologyEx(
        mascara_original, cv2.MORPH_OPEN, kernel, iterations=iteraciones
    )

    resultado = cv2.bitwise_and(frame, frame, mask=mascara_procesada)
    cv2.imshow("Morfologia", resultado)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
```

El programa completo permite cambiar color, operacion, vista, tamano de kernel e iteraciones.

---

## Concepto: que es morfologia

En vision por computadora, morfologia es un conjunto de operaciones que modifican la forma de las regiones blancas en una mascara binaria.

Una mascara binaria tiene:

| Valor | Significado |
|---|---|
| `255` | Pixel blanco, region seleccionada |
| `0` | Pixel negro, fondo |

Las operaciones morfologicas trabajan sobre esas regiones blancas.

La pregunta practica es:

```text
quiero hacer crecer, reducir, limpiar o cerrar las zonas blancas?
```

---

## Por que aparece despues de HSV

Los programas 12 y 13 crean mascaras por color. En la practica, esas mascaras rara vez quedan perfectas.

Pueden aparecer:

- puntos blancos aislados por ruido;
- huecos negros dentro del objeto;
- bordes quebrados;
- zonas del objeto perdidas por sombra;
- objetos cercanos parcialmente unidos.

La morfologia ayuda a preparar la mascara antes de buscar contornos.

---

## Pipeline del programa

```text
frame BGR
   |
   v
conversion a HSV
   |
   v
mascara por color con cv2.inRange
   |
   v
operacion morfologica
   |
   v
mascara procesada
   |
   v
resultado o contornos futuros
```

---

## Funciones nuevas en este programa

### `cv2.getStructuringElement(shape, ksize)`

Crea un kernel morfologico.

```python
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
```

| Parametro | Tipo | Descripcion |
|---|---|---|
| `shape` | `int` | Forma del kernel. |
| `ksize` | `tuple` | Tamano del kernel en formato `(ancho, alto)`. |

El kernel define la vecindad que OpenCV usara alrededor de cada pixel.

Un kernel rectangular de `3x3` se puede imaginar asi:

```text
[1][1][1]
[1][1][1]
[1][1][1]
```

Uno de `5x5` revisa una vecindad mas grande y por lo tanto produce un efecto mas fuerte.

---

### `cv2.erode(src, kernel, iterations=1)`

Aplica erosion. Reduce las zonas blancas.

```python
erosionada = cv2.erode(mascara, kernel, iterations=1)
```

Efectos:

- elimina puntos blancos pequenos;
- adelgaza objetos;
- separa objetos conectados por puentes delgados;
- puede destruir objetos pequenos si se usa de mas.

Regla intuitiva:

```text
para que un pixel quede blanco, su vecindad debe ser suficientemente blanca
```

---

### `cv2.dilate(src, kernel, iterations=1)`

Aplica dilatacion. Expande las zonas blancas.

```python
dilatada = cv2.dilate(mascara, kernel, iterations=1)
```

Efectos:

- rellena huecos pequenos;
- engrosa objetos;
- conecta partes cercanas;
- puede unir objetos separados si se usa de mas.

Regla intuitiva:

```text
si hay blanco cerca, el pixel puede volverse blanco
```

---

### `cv2.morphologyEx(src, op, kernel, iterations=1)`

Aplica operaciones morfologicas compuestas.

```python
apertura = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, kernel)
cierre = cv2.morphologyEx(mascara, cv2.MORPH_CLOSE, kernel)
```

| Operacion | Equivalencia | Uso principal |
|---|---|---|
| `cv2.MORPH_OPEN` | erosion + dilatacion | Quitar ruido blanco aislado |
| `cv2.MORPH_CLOSE` | dilatacion + erosion | Rellenar huecos negros pequenos |

---

## Operaciones del programa

### Sin morfologia

Muestra la mascara cruda tal como sale de `cv2.inRange`.

Sirve como punto de comparacion.

---

### Erosion

Reduce zonas blancas.

Es util cuando la mascara tiene puntos blancos sueltos en el fondo.

Problema comun: si el kernel es grande o hay muchas iteraciones, el objeto real puede desaparecer.

---

### Dilatacion

Expande zonas blancas.

Es util cuando el objeto queda cortado o tiene huecos pequenos.

Problema comun: puede unir regiones cercanas que deberian seguir separadas.

---

### Apertura

Apertura significa:

```text
erosion -> dilatacion
```

Es una de las operaciones mas utiles para limpiar ruido blanco.

Primero elimina puntos pequenos con erosion y luego intenta recuperar el tamano del objeto principal con dilatacion.

---

### Cierre

Cierre significa:

```text
dilatacion -> erosion
```

Es util para rellenar huecos negros dentro de un objeto.

Primero hace crecer las zonas blancas para cerrar huecos y luego reduce el crecimiento.

---

## Kernel e iteraciones

El programa permite cambiar el tamano del kernel:

```python
tamanios_kernel = [3, 5, 7, 9, 11, 15]
```

Tambien permite cambiar iteraciones:

```python
iteraciones = 1
```

Regla practica:

| Ajuste | Efecto |
|---|---|
| Kernel pequeno | Cambio suave |
| Kernel grande | Cambio fuerte |
| 1 iteracion | Efecto moderado |
| 2 o 3 iteraciones | Efecto mas agresivo |

Si se exagera, la mascara puede perder el objeto o unir regiones que no corresponden.

---

## Vistas del programa

| Vista | Que muestra |
|---|---|
| `Comparacion` | Mascara original y mascara procesada lado a lado |
| `Mascara original` | Mascara antes de morfologia |
| `Mascara procesada` | Mascara despues de morfologia |
| `Resultado` | Frame original filtrado con la mascara procesada |

La vista `Comparacion` es la mas util para aprender porque muestra directamente que cambio produjo la operacion.

---

## Interpretar el conteo de pixeles

El programa mide:

```python
pixeles_originales = cv2.countNonZero(mascara_original)
pixeles_procesados = cv2.countNonZero(mascara_procesada)
diferencia = pixeles_procesados - pixeles_originales
```

Si la diferencia es negativa, la operacion redujo la mascara.

Esto suele pasar con:

- erosion;
- apertura.

Si la diferencia es positiva, la operacion hizo crecer la mascara.

Esto suele pasar con:

- dilatacion;
- cierre.

---

## Errores comunes

### Usar morfologia sobre una imagen BGR

La morfologia de este programa debe aplicarse sobre la mascara binaria, no sobre el frame de color.

Correcto:

```python
mascara = cv2.inRange(hsv, bajo, alto)
procesada = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, kernel)
```

Incorrecto para este objetivo:

```python
procesada = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)
```

---

### Usar un kernel demasiado grande

Un kernel de `15x15` puede ser util, pero tambien puede destruir detalles pequenos.

Empieza con:

```text
3x3 o 5x5
```

---

### Confundir apertura con cierre

Usa esta regla:

```text
apertura -> abre espacio, quita ruido blanco
cierre   -> cierra huecos negros
```

---

## Ejemplos comentados

### Ejemplo 1: crear un kernel rectangular

```python
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
```

Comentario:

Este kernel revisa una vecindad de `5x5` alrededor de cada píxel.

```text
[1][1][1][1][1]
[1][1][1][1][1]
[1][1][1][1][1]
[1][1][1][1][1]
[1][1][1][1][1]
```

Mientras más grande sea el kernel, más fuerte será el efecto.

---

### Ejemplo 2: quitar puntos blancos con apertura

```python
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
mascara_limpia = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, kernel)
```

Comentario:

La apertura hace:

```text
erosion -> dilatacion
```

Uso típico:

```text
objeto blanco grande + ruido blanco pequeño -> objeto blanco grande
```

Si el ruido desaparece pero el objeto también se adelgaza demasiado, reduce el kernel a `3x3`.

---

### Ejemplo 3: cerrar huecos negros con cierre

```python
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
mascara_rellena = cv2.morphologyEx(mascara, cv2.MORPH_CLOSE, kernel)
```

Comentario:

El cierre hace:

```text
dilatacion -> erosion
```

Uso típico:

```text
objeto blanco con huecos negros pequeños -> objeto blanco más sólido
```

Si objetos separados se empiezan a unir, el kernel es demasiado grande o hay demasiadas iteraciones.

---

### Ejemplo 4: limpiar una máscara antes de contornos

```python
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

mascara = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, kernel)
mascara = cv2.morphologyEx(mascara, cv2.MORPH_CLOSE, kernel)
```

Comentario:

Este patrón es muy común:

```text
primero apertura -> quita ruido blanco
después cierre   -> rellena huecos
```

Es justo el tipo de preparación que conviene antes de `cv2.findContours`.

---

### Ejemplo 5: comparar kernel pequeño contra kernel grande

```python
kernel_3 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
kernel_9 = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))

suave = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, kernel_3)
fuerte = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, kernel_9)
```

Comentario:

`kernel_3` conserva más detalle, pero puede dejar ruido.

`kernel_9` limpia más agresivamente, pero puede borrar partes pequeñas del objeto.

---

### Ejemplo 6: medir el efecto con `countNonZero`

```python
antes = cv2.countNonZero(mascara_original)
despues = cv2.countNonZero(mascara_procesada)
diferencia = despues - antes

print(diferencia)
```

Comentario:

Interpretación:

| Diferencia | Posible significado |
|---:|---|
| Negativa | La operación redujo la región blanca |
| Positiva | La operación expandió la región blanca |
| Cerca de cero | Cambió la forma, pero no mucho el área total |

Esta medición no reemplaza la inspección visual, pero ayuda a entender el efecto de cada operación.

---

## Diferencia con programas anteriores

| Programa | Que hacia | Que aporta este programa |
|---|---|---|
| Programa 11 | Creaba mascaras por intensidad | Muestra como limpiar una mascara binaria |
| Programa 12 | Creaba mascaras por color HSV | Usa esas mascaras como entrada para morfologia |
| Programa 13 | Calibraba rangos HSV | Permite obtener una mascara base mejor antes de limpiarla |

---

## Relacion con el siguiente programa

El programa 15 usara contornos y cajas delimitadoras.

Ese flujo necesita una mascara lo mas clara posible:

```text
mascara HSV
  -> morfologia
  -> contornos
  -> bounding boxes
  -> area, centro y dimensiones
```

Si la mascara tiene ruido, los contornos detectaran regiones falsas. Si la mascara tiene huecos, el contorno puede salir fragmentado. Por eso este programa es el puente necesario antes de medir objetos.

---

## Conceptos clave

- La morfologia modifica regiones blancas en mascaras binarias.
- Erosion reduce blanco.
- Dilatacion expande blanco.
- Apertura elimina ruido blanco pequeno.
- Cierre rellena huecos negros pequenos.
- El kernel controla el tamano de la vecindad.
- Las iteraciones controlan cuantas veces se aplica la operacion.
- Una buena mascara facilita mucho la deteccion de contornos.
