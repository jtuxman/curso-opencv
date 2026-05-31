# Programa 08 — Grabar video en MKV

Igual que el programa 07 pero guarda en formato MKV usando el codec XVID. Presiona `r` para iniciar/detener la grabación, `q` para salir.

```python
import cv2
import time

cap = cv2.VideoCapture(0)

ancho = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
alto  = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps   = cap.get(cv2.CAP_PROP_FPS)

if fps == 0:
    fps = 30.0

fourcc  = cv2.VideoWriter_fourcc(*"XVID")
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

    cv2.imshow("Grabar MKV", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("r"):
        if not grabando:
            timestamp      = time.strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"video_{timestamp}.mkv"
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

## Diferencia con el Programa 07

Solo cambian dos cosas:

| Aspecto | Prog 07 (MP4) | Prog 08 (MKV) |
|---|---|---|
| Codec FourCC | `"mp4v"` | `"XVID"` |
| Extensión del archivo | `.mp4` | `.mkv` |

```python
# Programa 07:
fourcc         = cv2.VideoWriter_fourcc(*"mp4v")
nombre_archivo = f"video_{timestamp}.mp4"

# Programa 08:
fourcc         = cv2.VideoWriter_fourcc(*"XVID")
nombre_archivo = f"video_{timestamp}.mkv"
```

---

## Concepto: contenedor vs codec

Es importante distinguir dos conceptos que a menudo se confunden:

| Concepto | Descripción | Ejemplos |
|---|---|---|
| **Contenedor** | El formato del archivo — cómo se empaquetan los datos | `.mp4`, `.mkv`, `.avi` |
| **Codec** | El algoritmo de compresión del video | `XVID`, `H.264`, `MJPG` |

Un contenedor puede soportar múltiples codecs. Por ejemplo:
- `.mkv` puede contener video XVID, H.264, VP9, etc.
- `.mp4` puede contener H.264, MPEG-4, etc.

En OpenCV, **el codec se declara con FourCC** y la extensión del archivo define
el contenedor. OpenCV no siempre valida que el codec sea compatible con el
contenedor — si la combinación es incorrecta el archivo puede quedar vacío
o corrupto.

---

## Combinaciones probadas y confiables en Linux/Ubuntu

| Codec FourCC | Extensión | Notas |
|---|---|---|
| `mp4v` | `.mp4` | Compatible en casi todos los reproductores |
| `XVID` | `.mkv` | Buena calidad, funciona bien con VLC |
| `XVID` | `.avi` | El combo más clásico |
| `MJPG` | `.avi` | Frames JPEG concatenados, archivos grandes |
| `avc1` | `.mp4` | H.264 — mejor compresión, requiere soporte del sistema |

> **Por qué XVID para MKV:** XVID es un codec libre ampliamente soportado.
> MKV (Matroska) es un contenedor abierto sin restricciones de licencia.
> La combinación es robusta en Linux sin necesidad de librerías adicionales.

---

## Ventajas de MKV sobre MP4

| Característica | MKV | MP4 |
|---|---|---|
| Licencia | Libre y abierto | Patentes en algunos codecs |
| Recuperación ante cortes | Mejor — puede recuperarse si se corta la grabación | Puede corromperse si no se cierra bien |
| Soporte de subtítulos/capítulos | Nativo | Limitado |
| Compatibilidad con reproductores | Muy alta (VLC, MPV, etc.) | Universal |

> MKV es más resistente a corrupción si el programa termina abruptamente
> sin llamar `writer.release()`, aunque siempre es mejor cerrarlo correctamente.

---

## Conceptos clave

- El contenedor (`.mkv`) y el codec (`XVID`) son cosas distintas.
- Solo cambia el FourCC y la extensión respecto al programa 07 — la lógica es idéntica.
- `XVID` + `.mkv` es una combinación confiable en Linux sin dependencias extra.
- MKV tolera mejor los cierres abruptos que MP4.
