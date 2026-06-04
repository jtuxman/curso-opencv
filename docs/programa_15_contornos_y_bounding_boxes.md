# Programa 15 — Contornos y bounding boxes

Detecta objetos por color, limpia la mascara con morfologia y luego encuentra contornos para dibujar cajas delimitadoras, calcular area, centro y dimensiones.

Presiona `c` para cambiar color, `v` para cambiar vista, `r` para cambiar modo de recuperacion de contornos, `+` o `-` para ajustar el area minima y `q` para salir.

```python
import cv2

cap = cv2.VideoCapture(0)

area_minima = 1000
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

while True:
    ret, frame = cap.read()

    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Ejemplo: mascara para detectar verde.
    mascara = cv2.inRange(hsv, (35, 60, 60), (85, 255, 255))

    # Limpiar la mascara antes de buscar contornos.
    mascara = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, kernel)
    mascara = cv2.morphologyEx(mascara, cv2.MORPH_CLOSE, kernel)

    contornos, jerarquia = cv2.findContours(
        mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    for contorno in contornos:
        area = cv2.contourArea(contorno)

        if area < area_minima:
            continue

        x, y, w, h = cv2.boundingRect(contorno)
        momentos = cv2.moments(contorno)

        if momentos["m00"] != 0:
            cx = int(momentos["m10"] / momentos["m00"])
            cy = int(momentos["m01"] / momentos["m00"])
        else:
            cx = x + w // 2
            cy = y + h // 2

        cv2.drawContours(frame, [contorno], -1, (0, 255, 255), 2)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

    cv2.imshow("Contornos y bounding boxes", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
```

El programa completo agrega colores predefinidos, vistas, modo de recuperacion y ajuste interactivo de area minima.

---

## Objetivo

Hasta ahora el curso ha construido esta cadena:

```text
camara -> frame -> mascara -> mascara limpia
```

Este programa agrega la parte que convierte una mascara en objetos medibles:

```text
mascara limpia -> contornos -> cajas -> area, centro y dimensiones
```

Un contorno es el borde de una region blanca conectada en una mascara binaria. Si la mascara representa el objeto, el contorno representa su forma.

---

## Pipeline completo

```text
frame BGR
   |
   v
conversion a HSV
   |
   v
mascara por color
   |
   v
apertura + cierre
   |
   v
findContours
   |
   v
filtrar por area
   |
   v
boundingRect + moments
   |
   v
dibujar contorno, caja, centro y texto
```

Este flujo ya se parece a un detector simple de objetos. Todavia no usa inteligencia artificial, pero ya encuentra objetos segun reglas claras.

---

## Que es un contorno

Un contorno es una lista de puntos que rodean una region blanca.

Ejemplo conceptual:

```text
mascara:

0 0 0 0 0 0
0 0 255 255 0 0
0 255 255 255 255 0
0 0 255 255 0 0
0 0 0 0 0 0

contorno:

puntos que rodean la region blanca
```

OpenCV no devuelve el contorno como una imagen. Lo devuelve como un arreglo de puntos.

---

## Requisito fundamental: objeto blanco, fondo negro

`cv2.findContours` busca regiones blancas.

Por eso la mascara debe tener esta logica:

```text
objeto -> 255
fondo  -> 0
```

Si el objeto queda negro y el fondo blanco, OpenCV encontrara el fondo como el gran contorno principal.

En ese caso se puede invertir la mascara:

```python
mascara_invertida = cv2.bitwise_not(mascara)
```

O ajustar la segmentacion para que el objeto quede blanco.

---

## Funciones nuevas en este programa

### `cv2.findContours(image, mode, method)`

Encuentra contornos en una imagen binaria.

```python
contornos, jerarquia = cv2.findContours(
    mascara,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)
```

| Parametro | Tipo | Descripcion |
|---|---|---|
| `image` | `ndarray` | Mascara binaria de 1 canal. |
| `mode` | `int` | Como recuperar los contornos. |
| `method` | `int` | Como guardar los puntos del contorno. |

**Retorna:**

| Retorno | Descripcion |
|---|---|
| `contornos` | Lista de contornos encontrados. |
| `jerarquia` | Relacion entre contornos, util cuando hay contornos dentro de otros. |

Ejemplo comentado:

```python
# Buscar solo contornos externos.
# Si un objeto tiene un hueco interno, no se devuelve el hueco como contorno separado.
contornos, jerarquia = cv2.findContours(
    mascara,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)
```

---

### `cv2.RETR_EXTERNAL`

Recupera solo los contornos externos.

```python
contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
```

Es la opcion mas comun cuando se quiere una caja por objeto.

Ejemplo:

```text
un aro blanco tiene borde exterior y hueco interior

RETR_EXTERNAL -> solo devuelve el borde exterior
```

---

### `cv2.RETR_LIST`

Recupera todos los contornos sin organizar jerarquia.

```python
contornos, _ = cv2.findContours(mascara, cv2.RETR_LIST,
                                cv2.CHAIN_APPROX_SIMPLE)
```

Puede detectar contornos internos. Sirve para explorar, pero tambien puede generar mas regiones de las que se necesitan.

En el programa se cambia con `r`:

```text
Externos -> Todos -> Externos
```

---

### `cv2.CHAIN_APPROX_SIMPLE`

Comprime los puntos del contorno.

Un rectangulo no necesita guardar cada pixel de sus bordes. Basta con guardar sus esquinas principales.

```python
contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
```

Esto reduce memoria y suele ser suficiente.

Comparacion conceptual:

```text
CHAIN_APPROX_NONE:
guarda muchos puntos del borde

CHAIN_APPROX_SIMPLE:
guarda menos puntos, conservando la forma
```

---

### `cv2.contourArea(contour)`

Calcula el area de un contorno en pixeles cuadrados.

```python
area = cv2.contourArea(contorno)
```

Ejemplo comentado:

```python
for contorno in contornos:
    area = cv2.contourArea(contorno)

    # Ignorar regiones pequenas evita que puntos de ruido
    # se conviertan en objetos detectados.
    if area < 1000:
        continue
```

Importante: el area no esta en centimetros. Esta en pixeles.

Si el objeto se acerca a la camara, su area en pixeles aumenta. Si se aleja, disminuye.

---

### `cv2.boundingRect(contour)`

Calcula una caja recta que encierra el contorno.

```python
x, y, w, h = cv2.boundingRect(contorno)
```

| Valor | Significado |
|---|---|
| `x` | Coordenada horizontal de la esquina superior izquierda |
| `y` | Coordenada vertical de la esquina superior izquierda |
| `w` | Ancho de la caja |
| `h` | Alto de la caja |

Ejemplo comentado:

```python
x, y, w, h = cv2.boundingRect(contorno)

# Dibuja la caja desde la esquina superior izquierda
# hasta la esquina inferior derecha.
cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
```

La caja esta alineada con los ejes de la imagen. No rota con el objeto.

---

### `cv2.moments(contour)`

Calcula momentos geometricos del contorno.

```python
momentos = cv2.moments(contorno)
```

Los momentos permiten calcular el centroide:

```python
cx = int(momentos["m10"] / momentos["m00"])
cy = int(momentos["m01"] / momentos["m00"])
```

Donde:

| Momento | Significado practico |
|---|---|
| `m00` | Area del contorno |
| `m10` | Acumulacion horizontal ponderada |
| `m01` | Acumulacion vertical ponderada |

Ejemplo seguro:

```python
momentos = cv2.moments(contorno)

if momentos["m00"] != 0:
    cx = int(momentos["m10"] / momentos["m00"])
    cy = int(momentos["m01"] / momentos["m00"])
else:
    # Respaldo para evitar division entre cero.
    cx = x + w // 2
    cy = y + h // 2
```

El centroide es util para tracking, control de posicion y medicion de movimiento.

---

### `cv2.drawContours(image, contours, contourIdx, color, thickness)`

Dibuja contornos sobre una imagen.

```python
cv2.drawContours(frame, [contorno], -1, (0, 255, 255), 2)
```

| Parametro | Descripcion |
|---|---|
| `image` | Imagen donde se dibuja |
| `contours` | Lista de contornos |
| `contourIdx` | Indice del contorno a dibujar; `-1` dibuja todos |
| `color` | Color BGR |
| `thickness` | Grosor de la linea |

Ejemplos:

```python
# Dibujar todos los contornos en amarillo.
cv2.drawContours(frame, contornos, -1, (0, 255, 255), 2)

# Dibujar solo un contorno.
cv2.drawContours(frame, [contorno], -1, (0, 255, 255), 2)
```

---

## Ejemplo 1: detectar todos los contornos de una mascara

```python
contornos, _ = cv2.findContours(
    mascara,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)

print(f"Contornos encontrados: {len(contornos)}")
```

Comentario:

- Si aparecen demasiados contornos, probablemente hay ruido.
- Si no aparece ninguno, la mascara puede estar vacia.
- Si aparece un contorno enorme, quizas el fondo quedo blanco.

---

## Ejemplo 2: filtrar por area

```python
area_minima = 1000

for contorno in contornos:
    area = cv2.contourArea(contorno)

    if area < area_minima:
        continue

    print("Objeto candidato:", area)
```

Comentario:

Este filtro convierte muchos contornos pequenos en pocos objetos relevantes.

No existe un `area_minima` universal. Depende de:

- resolucion de la camara;
- distancia del objeto;
- tamano real del objeto;
- calidad de la mascara.

---

## Ejemplo 3: dibujar una caja delimitadora

```python
x, y, w, h = cv2.boundingRect(contorno)
cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
```

Comentario:

La caja ayuda a convertir una forma irregular en datos simples:

```text
posicion: (x, y)
tamano:   ancho x alto
```

Esto sera importante cuando avancemos a deteccion de objetos con modelos, porque muchos detectores devuelven cajas similares.

---

## Ejemplo 4: calcular centro del objeto

```python
momentos = cv2.moments(contorno)

if momentos["m00"] != 0:
    cx = int(momentos["m10"] / momentos["m00"])
    cy = int(momentos["m01"] / momentos["m00"])
else:
    cx = x + w // 2
    cy = y + h // 2

cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
```

Comentario:

El centro permite responder preguntas como:

- donde esta el objeto?
- se movio a la izquierda o derecha?
- esta cerca del centro de la imagen?
- como conecto este objeto con el frame siguiente?

Esto prepara el terreno para tracking.

---

## Ejemplo 5: obtener el objeto mas grande

```python
objetos = []

for contorno in contornos:
    area = cv2.contourArea(contorno)

    if area < 1000:
        continue

    objetos.append((area, contorno))

objetos.sort(reverse=True, key=lambda item: item[0])

if objetos:
    area_mayor, contorno_mayor = objetos[0]
    x, y, w, h = cv2.boundingRect(contorno_mayor)
```

Comentario:

Ordenar por area es una estrategia simple cuando se espera un objeto principal. No siempre es correcta, pero es util en escenarios controlados.

---

## Vistas del programa

| Vista | Que muestra |
|---|---|
| `Deteccion` | Frame con contornos, cajas, centros y texto |
| `Mascara` | Mascara limpia usada para buscar contornos |
| `Contornos` | Todos los contornos encontrados, sin filtro visual por area |
| `Original` | Frame original sin anotaciones |

La vista `Mascara` ayuda a diagnosticar. Si la mascara esta mal, la deteccion tambien estara mal.

---

## Area minima

El programa usa:

```python
area_minima = 1000
```

Y permite ajustarla con `+` y `-`.

Efecto:

| Area minima | Resultado |
|---:|---|
| Baja | Detecta mas regiones, incluido ruido |
| Alta | Detecta menos regiones, puede ignorar objetos pequenos |

Un buen valor depende de la escena. Por eso conviene ajustar mirando la vista `Deteccion` y la vista `Mascara`.

---

## Recuperacion de contornos

El programa permite alternar:

```text
Externos
Todos
```

### Externos

Usa:

```python
cv2.RETR_EXTERNAL
```

Es el modo recomendado para detectar objetos separados.

### Todos

Usa:

```python
cv2.RETR_LIST
```

Sirve para estudiar la mascara, pero puede detectar contornos internos que no representan objetos independientes.

---

## Errores comunes

### Buscar contornos sobre el frame BGR

Incorrecto para este flujo:

```python
contornos, _ = cv2.findContours(frame, cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
```

Correcto:

```python
contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
```

`findContours` debe recibir una imagen binaria de 1 canal.

---

### No limpiar la mascara

Si la mascara tiene ruido, cada punto blanco puede convertirse en un contorno.

Por eso el programa hace:

```python
mascara = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, kernel)
mascara = cv2.morphologyEx(mascara, cv2.MORPH_CLOSE, kernel)
```

Primero quita ruido blanco. Luego rellena huecos pequenos.

---

### Olvidar filtrar por area

Sin filtro:

```python
for contorno in contornos:
    x, y, w, h = cv2.boundingRect(contorno)
```

Esto puede dibujar cajas sobre puntos de ruido.

Con filtro:

```python
area = cv2.contourArea(contorno)

if area < area_minima:
    continue
```

---

### Confundir area con ancho por alto

`cv2.contourArea(contorno)` mide el area de la forma.

`w * h` mide el area de la caja.

Ejemplo:

```text
objeto triangular dentro de una caja:

area del contorno < area de la caja
```

Ambas medidas pueden ser utiles, pero no son iguales.

---

### Dividir entre cero con momentos

Esto puede fallar:

```python
cx = int(momentos["m10"] / momentos["m00"])
```

Si `m00` vale `0`, hay division entre cero.

Version segura:

```python
if momentos["m00"] != 0:
    cx = int(momentos["m10"] / momentos["m00"])
    cy = int(momentos["m01"] / momentos["m00"])
```

---

## Diferencia con programas anteriores

| Programa | Que hacia | Que aporta este programa |
|---|---|---|
| Programa 12 | Creaba mascara por color | Usa esa mascara para encontrar regiones |
| Programa 13 | Calibraba rangos HSV | Permite mejorar la mascara antes de medir |
| Programa 14 | Limpiaba la mascara | Convierte la mascara limpia en objetos medibles |

---

## Relacion con los siguientes programas

Este programa es la base para detectores hechos a mano.

Con area, centro y caja ya podemos crear reglas como:

```text
si color es verde
y area > 2000
y ancho/alto tiene cierta proporcion
entonces es un objeto candidato
```

El programa 16 usara esta idea para combinar color, tamano y forma.

---

## Conceptos clave

- Un contorno es el borde de una region blanca conectada.
- La mascara debe tener objeto blanco y fondo negro.
- `findContours` convierte una mascara en listas de puntos.
- `contourArea` mide el area de la forma.
- `boundingRect` calcula una caja delimitadora alineada con X/Y.
- `moments` permite calcular el centroide.
- Filtrar por area evita detectar ruido como objeto.
- Una buena mascara produce mejores contornos.
