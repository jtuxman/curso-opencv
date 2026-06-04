# Programa 12 — Segmentación por color en HSV

Detecta objetos por color usando el espacio HSV y máscaras creadas con `cv2.inRange`. Presiona `c` para cambiar el color objetivo, `m` para cambiar la vista y `q` para salir.

```python
import cv2

cap = cv2.VideoCapture(0)

colores = {
    "Rojo": [
        ((0, 80, 80), (10, 255, 255)),
        ((170, 80, 80), (179, 255, 255)),
    ],
    "Verde": [((35, 60, 60), (85, 255, 255))],
    "Azul": [((90, 60, 60), (130, 255, 255))],
    "Amarillo": [((20, 60, 60), (35, 255, 255))],
    "Naranja": [((10, 80, 80), (25, 255, 255))],
}

nombres_colores = list(colores.keys())
indice_color = 0

modos = ["Original", "Matiz", "Mascara", "Resultado"]
indice_modo = 0

while True:
    ret, frame = cap.read()

    if not ret:
        break

    color_objetivo = nombres_colores[indice_color]
    modo = modos[indice_modo]

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mascara = None

    for bajo, alto in colores[color_objetivo]:
        mascara_rango = cv2.inRange(hsv, bajo, alto)

        if mascara is None:
            mascara = mascara_rango
        else:
            mascara = cv2.bitwise_or(mascara, mascara_rango)

    resultado = cv2.bitwise_and(frame, frame, mask=mascara)

    hsv_matiz = hsv.copy()
    hsv_matiz[:, :, 1] = 255
    hsv_matiz[:, :, 2] = 255
    visual_matiz = cv2.cvtColor(hsv_matiz, cv2.COLOR_HSV2BGR)

    if modo == "Mascara":
        salida = cv2.cvtColor(mascara, cv2.COLOR_GRAY2BGR)
    elif modo == "Resultado":
        salida = resultado
    elif modo == "Matiz":
        salida = visual_matiz
    else:
        salida = frame

    cv2.imshow("Segmentacion por color HSV", salida)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("m"):
        indice_modo = (indice_modo + 1) % len(modos)
    elif key == ord("c"):
        indice_color = (indice_color + 1) % len(nombres_colores)
    elif key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
```

---

## Concepto: ¿qué es segmentar?

Segmentar significa separar una parte de la imagen que nos interesa.

En este programa, el criterio de separación es el color:

```text
pixeles del color objetivo -> blanco en la mascara
pixeles de otros colores   -> negro en la mascara
```

El resultado es una **máscara binaria**, igual que en el programa 11, pero ahora la decisión no se basa solo en brillo. Se basa en color.

---

## Por qué HSV y no BGR

OpenCV recibe la imagen de la cámara en BGR:

```python
frame  # canales B, G, R
```

En BGR, color y brillo están mezclados. Por ejemplo, un objeto rojo puede verse como:

```text
rojo iluminado: [B=20, G=40, R=230]
rojo oscuro:   [B=5,  G=15, R=90]
```

Ambos son rojos, pero sus valores BGR son muy diferentes.

HSV separa mejor el problema:

| Canal | Nombre | Rango en OpenCV | Qué representa |
|---|---|---:|---|
| `H` | Hue / Matiz | `0` a `179` | El color principal |
| `S` | Saturation / Saturación | `0` a `255` | Qué tan puro o intenso es el color |
| `V` | Value / Brillo | `0` a `255` | Qué tan claro u oscuro es |

Para detectar color, el canal más importante suele ser `H`.

---

## Pipeline del programa

```text
frame BGR
   │
   ▼ cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
frame HSV
   │
   ▼ cv2.inRange(hsv, bajo, alto)
mascara binaria
   │
   ▼ cv2.bitwise_and(frame, frame, mask=mascara)
resultado: solo se ve el color detectado
```

---

## Funciones nuevas en este programa

### `cv2.inRange(src, lowerb, upperb)`

Crea una máscara seleccionando los píxeles que están dentro de un rango.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `src` | `ndarray` | Imagen de entrada. En este programa es HSV. |
| `lowerb` | `tuple` | Valor mínimo permitido para cada canal. |
| `upperb` | `tuple` | Valor máximo permitido para cada canal. |

**Retorna:** imagen binaria de 1 canal.

Ejemplo:

```python
bajo = (35, 60, 60)
alto = (85, 255, 255)

mascara = cv2.inRange(hsv, bajo, alto)
```

La regla por píxel es:

```text
35 <= H <= 85
60 <= S <= 255
60 <= V <= 255
```

Si las tres condiciones se cumplen, el píxel queda blanco (`255`). Si alguna falla, queda negro (`0`).

---

### `cv2.bitwise_and(src1, src2, mask=mascara)`

Aplica una máscara sobre una imagen.

```python
resultado = cv2.bitwise_and(frame, frame, mask=mascara)
```

Como `src1` y `src2` son el mismo `frame`, el efecto práctico es:

```text
si mascara == 255 -> conserva el pixel original
si mascara == 0   -> deja el pixel negro
```

Esto permite ver el objeto detectado sobre fondo negro.

---

### `cv2.bitwise_or(src1, src2)`

Combina dos máscaras.

```python
mascara = cv2.bitwise_or(mascara_1, mascara_2)
```

La regla es:

```text
si una mascara tiene 255 -> resultado 255
si ambas tienen 0        -> resultado 0
```

En este programa se usa para el rojo, porque necesita dos rangos.

---

### `cv2.countNonZero(src)`

Cuenta cuántos píxeles distintos de cero hay en una imagen de 1 canal.

```python
pixeles_detectados = cv2.countNonZero(mascara)
```

Como la máscara solo tiene `0` y `255`, contar los valores distintos de cero equivale a contar los píxeles blancos.

El programa también calcula el porcentaje de la imagen detectada:

```python
total_pixeles = mascara.shape[0] * mascara.shape[1]
porcentaje = (pixeles_detectados / total_pixeles) * 100
```

Esto sirve como una primera medición simple:

```text
muchos píxeles blancos -> mucha imagen detectada
pocos píxeles blancos  -> poca imagen detectada
```

Más adelante, en contornos, esa medición será más precisa porque se hará por objeto detectado.

---

## El caso especial del rojo

En OpenCV, el canal `H` no va de `0` a `360`; va de `0` a `179`.

El rojo está alrededor de `0`, pero también aparece cerca del final de la escala:

```text
0 ... 10        -> rojo
170 ... 179     -> rojo
```

Por eso se definen dos rangos:

```python
"Rojo": [
    ((0, 80, 80), (10, 255, 255)),
    ((170, 80, 80), (179, 255, 255)),
]
```

Luego se combinan:

```python
mascara = cv2.bitwise_or(mascara_rojo_1, mascara_rojo_2)
```

Si solo se usa un rango para rojo, algunos tonos rojos no serán detectados.

---

## Rangos usados en el programa

Estos rangos son valores iniciales. Funcionan como punto de partida, no como una verdad universal.

| Color | Rango HSV |
|---|---|
| Rojo | `(0,80,80)-(10,255,255)` y `(170,80,80)-(179,255,255)` |
| Verde | `(35,60,60)-(85,255,255)` |
| Azul | `(90,60,60)-(130,255,255)` |
| Amarillo | `(20,60,60)-(35,255,255)` |
| Naranja | `(10,80,80)-(25,255,255)` |

La iluminación, la cámara y el material del objeto pueden cambiar estos valores.

Por eso el programa 13 agregará **trackbars** para calibrar los rangos en tiempo real.

---

## Vista de matiz

El programa incluye una vista llamada `Matiz`.

```python
hsv_matiz = hsv.copy()
hsv_matiz[:, :, 1] = 255
hsv_matiz[:, :, 2] = 255
visual_matiz = cv2.cvtColor(hsv_matiz, cv2.COLOR_HSV2BGR)
```

La idea es fijar saturación y brillo al máximo para visualizar mejor el canal `H`.

Esto ayuda a observar que:

- objetos de color parecido tienen matices similares;
- sombras cambian más el brillo que el matiz;
- zonas grises o blancas tienen saturación baja, por lo que su matiz puede ser poco útil.

---

## Por qué aparecen ruido y huecos

Este programa no limpia la máscara. Eso es intencional.

Pueden aparecer:

- puntos blancos aislados;
- huecos negros dentro del objeto;
- regiones detectadas por reflejos;
- zonas perdidas por sombras.

El siguiente paso natural será limpiar esas máscaras con operaciones morfológicas:

- erosión;
- dilatación;
- apertura;
- cierre.

Ese será el objetivo del programa 14. Antes, el programa 13 permitirá calibrar los rangos HSV con controles interactivos.

---

## Errores comunes

### Usar rangos HSV como si fueran RGB

Esto es incorrecto:

```python
bajo = (0, 0, 255)      # no significa rojo en HSV
alto = (50, 50, 255)
```

En HSV, la primera posición es matiz, no azul ni rojo:

```python
bajo = (0, 80, 80)
alto = (10, 255, 255)
```

---

### Olvidar convertir BGR a HSV

Esto produce una máscara sin sentido para rangos HSV:

```python
mascara = cv2.inRange(frame, bajo, alto)
```

Primero debe convertirse:

```python
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
mascara = cv2.inRange(hsv, bajo, alto)
```

---

### Usar un solo rango para rojo

El rojo necesita dos rangos en OpenCV:

```python
rojo_1 = cv2.inRange(hsv, (0, 80, 80), (10, 255, 255))
rojo_2 = cv2.inRange(hsv, (170, 80, 80), (179, 255, 255))
mascara = cv2.bitwise_or(rojo_1, rojo_2)
```

---

### Esperar que un rango fijo funcione siempre

Los rangos dependen de:

- iluminación;
- exposición automática de la cámara;
- balance de blancos;
- sombras;
- reflejos;
- color real del material.

Por eso los valores deben calibrarse en el ambiente donde se usará el detector.

---

## Ejemplos comentados

### Ejemplo 1: crear una máscara para un solo color

```python
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# Rango inicial para detectar verde.
bajo = (35, 60, 60)
alto = (85, 255, 255)

mascara = cv2.inRange(hsv, bajo, alto)
```

Comentario:

- `35` a `85` define el rango de matiz verde.
- `S min = 60` evita detectar blancos o grises como verde.
- `V min = 60` evita detectar zonas demasiado oscuras.
- Si el objeto verde no aparece completo, el rango puede estar muy cerrado.
- Si aparece mucho fondo, el rango puede estar demasiado abierto.

---

### Ejemplo 2: detectar rojo con dos rangos

```python
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

rojo_bajo_1 = (0, 80, 80)
rojo_alto_1 = (10, 255, 255)

rojo_bajo_2 = (170, 80, 80)
rojo_alto_2 = (179, 255, 255)

mascara_1 = cv2.inRange(hsv, rojo_bajo_1, rojo_alto_1)
mascara_2 = cv2.inRange(hsv, rojo_bajo_2, rojo_alto_2)

mascara_rojo = cv2.bitwise_or(mascara_1, mascara_2)
```

Comentario:

El rojo cruza el inicio y el final del canal `H`. Por eso se detecta en dos partes:

```text
0..10 y 170..179
```

Si solo usas un rango, algunos objetos rojos pueden desaparecer parcialmente.

---

### Ejemplo 3: aplicar una máscara sobre el frame original

```python
resultado = cv2.bitwise_and(frame, frame, mask=mascara)
```

Comentario:

Esta línea conserva los píxeles donde la máscara es blanca y pone negro donde la máscara es negra.

```text
mascara blanca -> se ve el pixel original
mascara negra  -> pixel negro
```

Es una forma rápida de verificar si la máscara está seleccionando el objeto correcto.

---

### Ejemplo 4: medir cuánta imagen fue detectada

```python
pixeles_detectados = cv2.countNonZero(mascara)
total_pixeles = mascara.shape[0] * mascara.shape[1]
porcentaje = (pixeles_detectados / total_pixeles) * 100

print(f"Detectado: {porcentaje:.1f}%")
```

Comentario:

Esta medición no identifica objetos todavía. Solo indica cuántos píxeles quedaron blancos.

Interpretación práctica:

| Resultado | Posible causa |
|---|---|
| `0%` | El rango no detecta el color |
| Muy bajo | El rango está muy cerrado o el objeto es pequeño |
| Muy alto | El rango está detectando fondo |
| Estable | La segmentación probablemente es usable |

---

### Ejemplo 5: diagnóstico rápido de una máscara HSV

```python
if porcentaje == 0:
    print("No se detecta nada: revisa H min/H max o baja S/V min")
elif porcentaje > 50:
    print("Demasiada imagen detectada: sube S min o reduce el rango H")
else:
    print("Rango posiblemente util para continuar")
```

Comentario:

No es una regla perfecta, pero ayuda al alumno a pensar en la máscara como una medición, no solo como una imagen.

---

## Diferencia con programas anteriores

| Programa | Qué hacía | Qué aporta este programa |
|---|---|---|
| Programa 05 | Mostraba espacios de color | Usa HSV para tomar decisiones por color |
| Programa 11 | Umbralizaba por intensidad | Umbraliza por rangos de color |
| Programa 10 | Aplicaba filtros | Muestra que el ruido visual puede afectar las máscaras |

---

## Relación con los siguientes programas

Este programa es la base de los primeros detectores de objetos.

El flujo futuro será:

```text
segmentar por color
  -> calibrar rangos HSV
  -> limpiar mascara
  -> encontrar contornos
  -> dibujar cajas
  -> medir posicion y tamano
```

Los siguientes programas conectan con este:

- `programa_13_trackbars_hsv.py`: ajustar rangos HSV en tiempo real;
- `programa_14_morfologia.py`: limpiar ruido y huecos de la máscara;
- `programa_15_contornos_y_bounding_boxes.py`: medir el objeto detectado.

---

## Conceptos clave

- HSV separa matiz, saturación y brillo.
- `H` identifica el color, pero en OpenCV va de `0` a `179`.
- `cv2.inRange` crea máscaras por rango.
- `cv2.bitwise_and` aplica una máscara sobre la imagen original.
- El rojo necesita dos rangos por estar en los extremos del canal `H`.
- Una máscara ruidosa no significa que el método falle; significa que debe calibrarse o limpiarse.
