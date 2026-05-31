# Programa 07 — Grabar video en MP4

Graba el video de la cámara a un archivo `.mp4`. Presiona `r` para iniciar y detener la grabación. El estado se muestra en pantalla en verde (en espera) o rojo (grabando).

```python
import cv2
import time

cap = cv2.VideoCapture(0)

ancho = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
alto  = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps   = cap.get(cv2.CAP_PROP_FPS)

if fps == 0:
    fps = 30.0

fourcc  = cv2.VideoWriter_fourcc(*"mp4v")
grabando = False
writer   = None

while True:
    ret, frame = cap.read()

    if not ret:
        break

    if grabando and writer is not None:
        writer.write(frame)

    estado = "GRABANDO" if grabando else "EN ESPERA"
    color  = (0, 0, 255) if grabando else (0, 255, 0)
    cv2.putText(frame, estado, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    cv2.imshow("Grabar video", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("r"):
        if not grabando:
            timestamp      = time.strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"video_{timestamp}.mp4"
            writer  = cv2.VideoWriter(nombre_archivo, fourcc, fps, (ancho, alto))
            grabando = True
        else:
            grabando = False
            writer.release()
            writer = None

    elif key == ord("q"):
        break

if writer is not None:
    writer.release()

cap.release()
cv2.destroyAllWindows()
```

---

## Concepto: contenedor vs codec

Al grabar video, hay dos conceptos distintos que trabajan juntos:

| Concepto | Qué es | Ejemplos |
|---|---|---|
| **Contenedor** | El formato del archivo — cómo se empaquetan y sincronizan los datos | `.mp4`, `.mkv`, `.avi` |
| **Codec** | El algoritmo que comprime los frames de video | `mp4v`, `XVID`, `H.264` |

```
Archivo .mp4
└── Contenedor MP4
    ├── Pista de video comprimida con codec mp4v
    └── (opcionalmente) Pista de audio
```

En OpenCV: la **extensión** define el contenedor y el **FourCC** define el codec.

---

## Funciones nuevas en este programa

### `cv2.VideoWriter_fourcc(*codec)`

Crea el código FourCC (Four Character Code) que identifica el codec de video.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `*codec` | `str` | Los 4 caracteres del codec. El `*` desempaqueta la cadena en 4 argumentos. |

**Retorna:** `int` — código numérico del codec para pasar a `VideoWriter`.

**Ejemplos:**

```python
# El * desempaqueta la cadena en caracteres individuales:
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
# equivalente a:
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

# Codecs más comunes:
fourcc_mp4  = cv2.VideoWriter_fourcc(*"mp4v")   # MPEG-4, para .mp4
fourcc_xvid = cv2.VideoWriter_fourcc(*"XVID")   # XVID, para .avi o .mkv
fourcc_mjpg = cv2.VideoWriter_fourcc(*"MJPG")   # Motion JPEG, para .avi
fourcc_h264 = cv2.VideoWriter_fourcc(*"avc1")   # H.264, para .mp4 (requiere soporte)

# Tabla de combinaciones confiables en Linux/Ubuntu:
# fourcc "mp4v" + extensión .mp4 → funciona en casi todos los reproductores
# fourcc "XVID" + extensión .avi → clásico, muy compatible
# fourcc "XVID" + extensión .mkv → buena calidad, libre de licencias
# fourcc "MJPG" + extensión .avi → rápido, archivos grandes
```

---

### `cv2.VideoWriter(filename, fourcc, fps, frameSize)`

Crea un objeto que escribe frames en un archivo de video.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `filename` | `str` | Nombre y ruta del archivo de salida. La extensión define el contenedor. |
| `fourcc` | `int` | Código del codec obtenido con `VideoWriter_fourcc`. |
| `fps` | `float` | Frames por segundo del video de salida. Debe coincidir con la cámara. |
| `frameSize` | `tuple (ancho, alto)` | Dimensiones de cada frame. **Orden: (ancho, alto)**, no (alto, ancho). |

**Retorna:** objeto `VideoWriter`.

**Ejemplos:**

```python
fourcc = cv2.VideoWriter_fourcc(*"mp4v")

# Creación básica:
writer = cv2.VideoWriter("salida.mp4", fourcc, 30.0, (640, 480))

# Con dimensiones de la cámara:
ancho = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
alto  = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps   = cap.get(cv2.CAP_PROP_FPS) or 30.0
writer = cv2.VideoWriter("salida.mp4", fourcc, fps, (ancho, alto))

# ERROR frecuente — ancho y alto invertidos:
writer = cv2.VideoWriter("salida.mp4", fourcc, fps, (alto, ancho))   # MAL
writer = cv2.VideoWriter("salida.mp4", fourcc, fps, (ancho, alto))   # BIEN

# Verificar si se creó correctamente:
if not writer.isOpened():
    print("Error: no se pudo crear el archivo de video")

# Para video en escala de grises (isColor=False):
writer = cv2.VideoWriter("gris.avi", fourcc, fps, (ancho, alto), isColor=False)
```

---

### `writer.write(frame)`

Escribe un frame al archivo de video.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `frame` | `ndarray` | Frame en formato BGR. Debe tener exactamente las dimensiones declaradas en `VideoWriter`. |

**Sin valor de retorno.**

**Ejemplos:**

```python
# Escritura básica:
writer.write(frame)

# Si el frame tiene dimensiones diferentes, el video se corrompe silenciosamente:
# writer fue creado con (640, 480) pero frame es (720, 1280) → problema
# Solución: redimensionar antes de escribir:
frame_resized = cv2.resize(frame, (ancho, alto))
writer.write(frame_resized)

# Grabar solo cada N frames (para reducir tamaño del archivo):
contador_frames = 0
while True:
    ret, frame = cap.read()
    contador_frames += 1
    if contador_frames % 2 == 0:   # grabar 1 de cada 2 frames
        writer.write(frame)
```

---

### `writer.release()`

Finaliza la escritura y cierra el archivo correctamente.

**Sin parámetros. Sin valor de retorno.**

**Ejemplos:**

```python
writer.release()

# Sin release(), el archivo MP4 queda sin los headers finales
# y muchos reproductores no pueden abrirlo.

# Patrón recomendado con salvaguarda:
try:
    while True:
        ret, frame = cap.read()
        if grabando:
            writer.write(frame)
        # ...
finally:
    if writer is not None:
        writer.release()    # se ejecuta siempre, incluso si hay excepción
    cap.release()
    cv2.destroyAllWindows()
```

---

## Por qué verificar `fps == 0`

```python
fps = cap.get(cv2.CAP_PROP_FPS)

if fps == 0:
    fps = 30.0
```

Algunas cámaras o drivers retornan `0` para `CAP_PROP_FPS`. Si se pasa `fps=0` a `VideoWriter`:
- El archivo se crea sin errores visibles.
- Al reproducirlo, todos los frames aparecen sin tiempo entre ellos (el video se ve instantáneo o corrupte).

Usar `30.0` como valor de respaldo es seguro porque la mayoría de webcams trabajan a 30 fps.

---

## Flujo de grabación

```
Tecla 'r' (grabando=False)
    │
    ▼
Crear VideoWriter → grabando = True
    │
    ▼
Loop: writer.write(frame) en cada iteración
    │
    ▼
Tecla 'r' (grabando=True)
    │
    ▼
grabando=False → writer.release() → writer=None
    │
    ▼ (puede iniciar otra grabación con 'r' de nuevo)
```

---

## Conceptos clave

- `VideoWriter_fourcc(*"mp4v")` — el `*` desempaqueta la cadena en 4 caracteres.
- `frameSize` en `VideoWriter` es `(ancho, alto)` — NO `(alto, ancho)`.
- Siempre llamar `writer.release()` para no corromper el archivo.
- Verificar `fps != 0` antes de crear el `VideoWriter`.
- El `writer` se crea al iniciar la grabación y se destruye al detenerla, permitiendo múltiples clips por sesión.
