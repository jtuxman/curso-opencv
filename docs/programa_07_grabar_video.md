# Programa 07 — Grabar video

Graba el video de la cámara a un archivo `.mp4`. Presiona `r` para iniciar y detener la grabación. El estado se muestra en pantalla en verde (en espera) o rojo (grabando). Presiona `q` para salir.

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
            timestamp     = time.strftime("%Y%m%d_%H%M%S")
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

## Funciones nuevas en este programa

### `cv2.VideoWriter_fourcc(*codec)`

Crea un código de cuatro caracteres (FourCC) que identifica el codec de video.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `*codec` | `str` | Cuatro caracteres del codec, pasados como argumentos separados con `*`. |

**Retorna:** `int` — código numérico del codec para usar en `VideoWriter`.

```python
fourcc = cv2.VideoWriter_fourcc(*"mp4v")   # MP4 (más compatible)
fourcc = cv2.VideoWriter_fourcc(*"XVID")   # AVI con XVID
fourcc = cv2.VideoWriter_fourcc(*"MJPG")   # Motion JPEG (AVI)
```

#### ¿Qué es FourCC?

FourCC (Four Character Code) es un identificador estándar de 4 bytes que le dice
al sistema qué algoritmo de compresión usar para codificar el video.

| Codec | Extensión | Descripción |
|---|---|---|
| `mp4v` | `.mp4` | MPEG-4 — buena compresión, muy compatible |
| `XVID` | `.avi` | XVID — calidad alta, archivo más grande |
| `MJPG` | `.avi` | Motion JPEG — rápido pero archivos grandes |
| `avc1` | `.mp4` | H.264 — mejor compresión (requiere soporte del sistema) |

> **El `*` en `*"mp4v"`:** desempaqueta la cadena en 4 argumentos individuales
> `'m', 'p', '4', 'v'`. Es equivalente a `cv2.VideoWriter_fourcc('m','p','4','v')`.

---

### `cv2.VideoWriter(filename, fourcc, fps, frameSize)`

Crea un objeto para escribir frames en un archivo de video.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `filename` | `str` | Nombre y ruta del archivo de salida. |
| `fourcc` | `int` | Codec obtenido con `VideoWriter_fourcc`. |
| `fps` | `float` | Frames por segundo del video de salida. |
| `frameSize` | `tuple (ancho, alto)` | Dimensiones de cada frame. |

**Retorna:** objeto `VideoWriter`.

```python
writer = cv2.VideoWriter("salida.mp4", fourcc, 30.0, (640, 480))
```

> **Importante:** `frameSize` es `(ancho, alto)` — orden inverso a `frame.shape`
> que retorna `(alto, ancho)`. Este es un error muy común.

```python
# Correcto:
ancho = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
alto  = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
writer = cv2.VideoWriter("salida.mp4", fourcc, fps, (ancho, alto))

# Error frecuente (ancho y alto invertidos):
writer = cv2.VideoWriter("salida.mp4", fourcc, fps, (alto, ancho))  # MAL
```

---

### `writer.write(frame)`

Escribe un frame en el archivo de video.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `frame` | `ndarray` | Frame en formato BGR con las dimensiones declaradas en `VideoWriter`. |

**Sin valor de retorno.**

```python
writer.write(frame)
```

> El frame debe tener exactamente el mismo tamaño que `frameSize` declarado
> al crear el `VideoWriter`. Si difiere, el video se corrompe o no se escribe.

---

### `writer.release()`

Finaliza la escritura y cierra el archivo de video correctamente.

**Sin parámetros. Sin valor de retorno.**

```python
writer.release()
```

> **Crítico:** si el programa termina sin llamar `writer.release()`, el archivo
> puede quedar corrupto o incompleto (sin los headers finales del contenedor MP4).
> Por eso el programa también lo llama fuera del loop como salvaguarda:
> ```python
> if writer is not None:
>     writer.release()
> ```

---

## Flujo de grabación

```
Tecla 'r' (grabando=False)
    │
    ▼
Crear VideoWriter  →  grabando = True
    │
    ▼
Loop: writer.write(frame) en cada iteración
    │
    ▼
Tecla 'r' (grabando=True)
    │
    ▼
grabando = False  →  writer.release()  →  writer = None
```

---

## Por qué se verifica `fps == 0`

Algunas cámaras o drivers no reportan correctamente los FPS:

```python
fps = cap.get(cv2.CAP_PROP_FPS)

if fps == 0:
    fps = 30.0
```

Si se pasa `fps=0` a `VideoWriter`, el video se crea pero reproduce de forma
incorrecta. El valor de 30.0 es el estándar más común para webcams.

---

## Diferencia con programas anteriores

| Aspecto | Prog 03 (captura) | Prog 07 (video) |
|---|---|---|
| Guarda | Una imagen PNG | Secuencia de frames como MP4 |
| Función de guardado | `cv2.imwrite()` | `writer.write()` en cada frame |
| Necesita liberar | No (imagen estática) | Sí, `writer.release()` obligatorio |
| Codec | No aplica | FourCC (`mp4v`, `XVID`...) |
| FPS | No aplica | Debe coincidir con la cámara |

---

## Conceptos clave

- `VideoWriter_fourcc(*"mp4v")` define el codec; el `*` desempaqueta la cadena.
- `frameSize` en `VideoWriter` es `(ancho, alto)` — no `(alto, ancho)`.
- Siempre llamar `writer.release()` para no corromper el archivo.
- Verificar que `fps != 0` antes de crear el `VideoWriter`.
- El `writer` se crea al iniciar la grabación y se destruye al detenerla, permitiendo grabar múltiples clips en la misma sesión.
