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

Abre un dispositivo de captura de video y devuelve un objeto para controlarlo.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `index` | `int` o `str` | Índice de la cámara o ruta de un archivo de video. |

**Retorna:** objeto `VideoCapture`. Si no pudo abrirse, el objeto existe pero `cap.isOpened()` retorna `False`.

**Ejemplos:**

```python
cap = cv2.VideoCapture(0)           # cámara por defecto (integrada)
cap = cv2.VideoCapture(1)           # segunda cámara (USB externa)
cap = cv2.VideoCapture(2)           # tercera cámara
cap = cv2.VideoCapture("video.mp4") # archivo de video en disco
cap = cv2.VideoCapture("rtsp://ip/stream") # cámara IP por red

# Verificar si se abrió correctamente:
if not cap.isOpened():
    print("No se pudo abrir la cámara")
```

---

### `cap.read()`

Lee el siguiente frame disponible de la cámara o archivo de video.

**No recibe parámetros.**

**Retorna:** tupla `(ret, frame)`

| Variable | Tipo | Descripción |
|---|---|---|
| `ret` | `bool` | `True` si el frame se leyó correctamente. `False` si la cámara se desconectó o el video terminó. |
| `frame` | `numpy.ndarray` | Array de forma `(alto, ancho, 3)` en formato BGR. Cada valor es `uint8` (0-255). |

**Ejemplos:**

```python
ret, frame = cap.read()

# Verificar antes de usar el frame:
if not ret:
    break  # salir del loop si no hay frame válido

# El frame es un array NumPy; se puede inspeccionar:
print(frame.shape)   # → (480, 640, 3) = (alto, ancho, canales)
print(frame.dtype)   # → uint8
print(frame[0, 0])   # → [B, G, R] del pixel en la esquina superior izquierda

# Acceder a un canal específico:
canal_azul  = frame[:, :, 0]  # todos los pixeles, canal B
canal_verde = frame[:, :, 1]  # todos los pixeles, canal G
canal_rojo  = frame[:, :, 2]  # todos los pixeles, canal R
```

> **Nota:** OpenCV usa **BGR** (Azul, Verde, Rojo) en lugar del RGB convencional.
> Si se envía el frame a otra librería como matplotlib o Pillow, hay que convertirlo:
> ```python
> rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
> ```

---

### `cv2.imshow(nombre_ventana, imagen)`

Muestra una imagen en una ventana en pantalla.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `nombre_ventana` | `str` | Título de la ventana. Si no existe, la crea automáticamente. |
| `imagen` | `numpy.ndarray` | Frame o imagen a mostrar. Puede ser 1 canal (gris) o 3 canales (BGR). |

**Ejemplos:**

```python
cv2.imshow("Camara", frame)              # ventana llamada "Camara"
cv2.imshow("Procesado", frame_gris)      # segunda ventana independiente

# Mostrar múltiples ventanas simultáneamente:
cv2.imshow("Original", frame)
cv2.imshow("Bordes", frame_bordes)
cv2.imshow("Filtrado", frame_filtro)
# Cada llamada abre su propia ventana con su propio título
```

> **Importante:** `imshow` por sí sola NO refresca la ventana. Necesita que
> `cv2.waitKey()` se llame en el mismo hilo para que la imagen se actualice.

---

### `cv2.waitKey(delay)`

Espera un tiempo y captura la tecla presionada. Es el "latido" del loop de OpenCV.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `delay` | `int` | Milisegundos a esperar. `0` = espera infinita. `1` = espera mínima (para video en tiempo real). |

**Retorna:** `int` con el código ASCII de la tecla presionada, o `-1` si no se presionó ninguna.

**Ejemplos:**

```python
cv2.waitKey(1)    # loop de cámara en tiempo real (~60+ fps posibles)
cv2.waitKey(33)   # ~30 fps (1000ms / 30 = 33ms por frame)
cv2.waitKey(0)    # espera indefinida; útil para ver una imagen fija

# Capturar qué tecla se presionó:
key = cv2.waitKey(1) & 0xFF

if key == ord("q"):          # salir
    break
elif key == ord("s"):        # guardar
    cv2.imwrite("foto.png", frame)
elif key == ord("f"):        # otra acción
    frame = cv2.flip(frame, 1)

# Detectar teclas especiales (flechas, F1, etc.):
key = cv2.waitKey(1)
if key == 81:    # flecha izquierda (Linux)
    pass
if key == 83:    # flecha derecha (Linux)
    pass
```

> **¿Por qué `& 0xFF`?**
> En algunos sistemas `waitKey` retorna un valor de 32 bits donde los bits
> superiores contienen flags del sistema operativo. La máscara `0xFF`
> (= `11111111` en binario) conserva solo los 8 bits menos significativos,
> que son los que representan el código ASCII de la tecla.
>
> ```
> waitKey retorna: 0x00FF0071  (en algunos sistemas Linux de 64 bits)
>          & 0xFF: 0x00000071  = 113 = ord("q")
> ```

---

### `cap.release()`

Libera el dispositivo de captura y cierra la conexión con la cámara.

**Sin parámetros. Sin valor de retorno.**

```python
cap.release()

# Sin llamar release(), la cámara queda bloqueada:
# - Otros programas no pueden abrirla
# - El LED de la cámara puede quedar encendido
# - Al volver a ejecutar el script puede fallar al abrirla

# Patrón recomendado con manejo de errores:
try:
    while True:
        ret, frame = cap.read()
        # ... procesamiento ...
finally:
    cap.release()           # se ejecuta siempre, incluso si hay excepción
    cv2.destroyAllWindows()
```

---

### `cv2.destroyAllWindows()`

Cierra todas las ventanas de OpenCV abiertas.

**Sin parámetros. Sin valor de retorno.**

```python
cv2.destroyAllWindows()           # cierra todas las ventanas

# Alternativa: cerrar solo una ventana específica:
cv2.destroyWindow("Camara")       # cierra la ventana llamada "Camara"
cv2.destroyWindow("Procesado")    # cierra otra ventana

# En algunos sistemas (especialmente Windows) las ventanas no se cierran
# visualmente hasta que se llama destroyAllWindows() + waitKey():
cv2.destroyAllWindows()
cv2.waitKey(1)   # fuerza el procesamiento de eventos de ventana
```

---

## Flujo del programa

```
VideoCapture(0)  ← abre la cámara
      │
      ▼
  cap.read() ──► ret == False ──► break ──► cap.release()
      │                                          │
   ret == True                        destroyAllWindows()
      │
      ▼
  imshow(frame)  ← muestra el frame en pantalla
      │
      ▼
  waitKey(1) ──► tecla 'q' ──► break
      │
   otra tecla / sin tecla
      │
      ▼
  (siguiente iteración del while)
```

---

## Conceptos clave

- El frame es un array **NumPy** — se puede manipular con todas las operaciones matriciales de NumPy.
- OpenCV usa **BGR**, no RGB — importante al combinar con otras librerías.
- `waitKey(1)` es **obligatorio** en el loop; sin él la ventana no se refresca y el programa se congela.
- Siempre llamar `cap.release()` para no dejar la cámara ocupada.
- `ret` debe verificarse antes de usar `frame`; si es `False` el frame contiene datos inválidos.
