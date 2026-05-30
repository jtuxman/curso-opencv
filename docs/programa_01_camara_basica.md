# Programa 01 — Cámara básica

Muestra en tiempo real el contenido de la cámara web. Presiona `q` para salir.

```python
import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        print("No se pudo leer el frame")
        break

    cv2.imshow("Camara", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
```

---

## Funciones usadas

### `cv2.VideoCapture(index)`

Abre un dispositivo de captura de video.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `index` | `int` | Índice de la cámara. `0` = cámara por defecto, `1`, `2`... para otras. |

**Retorna:** objeto `VideoCapture`.

```python
cap = cv2.VideoCapture(0)   # cámara integrada
cap = cv2.VideoCapture(1)   # segunda cámara
cap = cv2.VideoCapture("video.mp4")  # también acepta archivos de video
```

---

### `cap.read()`

Lee el siguiente frame de la cámara.

**No recibe parámetros.**

**Retorna:** tupla `(ret, frame)`

| Variable | Tipo | Descripción |
|---|---|---|
| `ret` | `bool` | `True` si el frame se leyó correctamente, `False` si hubo error. |
| `frame` | `numpy.ndarray` | Imagen del frame en formato BGR (no RGB). Array de forma `(alto, ancho, 3)`. |

```python
ret, frame = cap.read()

if not ret:
    break  # sin señal o cámara desconectada
```

> **Nota:** OpenCV usa BGR (Azul, Verde, Rojo) en lugar del RGB convencional.
> Para convertir: `rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)`

---

### `cv2.imshow(nombre_ventana, imagen)`

Muestra una imagen en una ventana en pantalla.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `nombre_ventana` | `str` | Título de la ventana. Si no existe, la crea. |
| `imagen` | `numpy.ndarray` | Frame o imagen a mostrar. |

```python
cv2.imshow("Camara", frame)
cv2.imshow("Otra ventana", frame2)  # se pueden tener múltiples ventanas
```

---

### `cv2.waitKey(delay)`

Espera un tiempo y captura la tecla presionada.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `delay` | `int` | Milisegundos a esperar. `0` = espera indefinida hasta que se presione una tecla. `1` = mínimo delay (necesario para que la ventana se refresque). |

**Retorna:** `int` con el código ASCII de la tecla presionada, o `-1` si no se presionó ninguna.

```python
key = cv2.waitKey(1)          # espera 1ms
key = cv2.waitKey(0)          # espera hasta que el usuario presione algo

if cv2.waitKey(1) & 0xFF == ord("q"):
    break
```

> **Por qué `& 0xFF`:** en algunos sistemas `waitKey` retorna un valor de 32 bits.
> El `& 0xFF` aplica una máscara para quedarse solo con el byte menos significativo
> (los 8 bits que representan el código ASCII), haciendo la comparación compatible
> en todos los sistemas operativos.

---

### `cap.release()`

Libera el dispositivo de captura y cierra la conexión con la cámara.

**Sin parámetros. Sin valor de retorno.**

Siempre llamarlo al terminar para liberar el recurso del sistema operativo.

```python
cap.release()
```

---

### `cv2.destroyAllWindows()`

Cierra todas las ventanas de OpenCV abiertas.

**Sin parámetros. Sin valor de retorno.**

```python
cv2.destroyAllWindows()          # cierra todas
cv2.destroyWindow("Camara")      # cierra solo una ventana por nombre
```

---

## Flujo del programa

```
VideoCapture(0)
      |
      v
  cap.read() ──► ret == False ──► break
      |
   ret == True
      |
      v
  imshow(frame)
      |
      v
  waitKey(1) ──► tecla 'q' ──► break
      |
   otra tecla
      |
      v
  (siguiente iteración)
      |
      v
cap.release()
destroyAllWindows()
```

---

## Conceptos clave

- El frame es un array NumPy — se puede manipular con operaciones de matrices.
- OpenCV usa **BGR**, no RGB.
- `waitKey(1)` es obligatorio en el loop; sin él la ventana no se refresca.
- Siempre llamar `cap.release()` para no dejar la cámara ocupada.
