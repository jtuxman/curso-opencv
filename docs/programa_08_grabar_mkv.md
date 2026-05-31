# Programa 08 — Grabar video en MKV con efecto espejo

Graba en formato MKV con codec XVID. El video se graba en espejo (volteado horizontalmente). Presiona `r` para iniciar/detener la grabación, `q` para salir.

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

    frame = cv2.flip(frame, 1)     # voltear antes de grabar y mostrar

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

## Diferencias respecto al Programa 07

Este programa añade dos cambios sobre el programa 07:

### Cambio 1: codec y extensión (MP4 → MKV)

```python
# Programa 07 (MP4):
fourcc         = cv2.VideoWriter_fourcc(*"mp4v")
nombre_archivo = f"video_{timestamp}.mp4"

# Programa 08 (MKV):
fourcc         = cv2.VideoWriter_fourcc(*"XVID")
nombre_archivo = f"video_{timestamp}.mkv"
```

### Cambio 2: efecto espejo antes de grabar

```python
frame = cv2.flip(frame, 1)   # se aplica ANTES de writer.write()

if grabando and writer is not None:
    writer.write(frame)      # graba el frame ya volteado
```

> **Por qué el orden importa:**
> Si `flip` se aplica **antes** de `write`, el video grabado queda en espejo.
> Si `flip` se aplica **después** de `write`, la pantalla muestra espejo pero el archivo graba la imagen original.

---

## Concepto: contenedor MKV vs MP4

| Característica | MKV (Matroska) | MP4 |
|---|---|---|
| Licencia | Completamente libre y abierto | Algunas partes con patentes |
| Resistencia a corrupción | Alta — puede recuperar video si se corta | Menor — puede corromperse sin `release()` |
| Soporte de múltiples pistas | Nativo (video, audio, subtítulos, capítulos) | Limitado |
| Compatibilidad | Muy alta (VLC, MPV, Firefox, etc.) | Universal |
| Uso típico | Video general en Linux | Distribución masiva, web, móvil |

### ¿Por qué MKV es más resistente a corrupción?

MP4 escribe los metadatos (índice de frames, duración, etc.) **al final del archivo** cuando se llama `release()`. Si el programa termina abruptamente sin llamarlo, esos metadatos nunca se escriben y el archivo queda ilegible.

MKV escribe los metadatos **de forma distribuida** a lo largo del archivo. Si se interrumpe, la mayoría del video ya grabado es recuperable.

---

## Codec XVID

XVID es una implementación libre del estándar de compresión MPEG-4 Part 2.

```python
fourcc = cv2.VideoWriter_fourcc(*"XVID")
```

| Característica | XVID |
|---|---|
| Licencia | GPL (libre) |
| Calidad | Alta para su tamaño |
| Velocidad de codificación | Rápida |
| Compatibilidad | Muy alta (VLC, reproductores de TV, etc.) |
| Extensiones | `.avi`, `.mkv` |

**Comparación con otros codecs:**

```python
# mp4v → MPEG-4 Part 2, mejor con .mp4
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
writer = cv2.VideoWriter("salida.mp4", fourcc, fps, (ancho, alto))

# XVID → MPEG-4 Part 2 libre, mejor con .avi o .mkv
fourcc = cv2.VideoWriter_fourcc(*"XVID")
writer = cv2.VideoWriter("salida.mkv", fourcc, fps, (ancho, alto))

# MJPG → frames JPEG concatenados, archivos grandes pero rápido de codificar
fourcc = cv2.VideoWriter_fourcc(*"MJPG")
writer = cv2.VideoWriter("salida.avi", fourcc, fps, (ancho, alto))
```

---

## Tabla resumen: combinaciones de codec + contenedor en Linux

| Codec FourCC | Extensión | Resultado |
|---|---|---|
| `mp4v` | `.mp4` | Compatible en casi todos los reproductores |
| `XVID` | `.mkv` | Este programa — libre y resistente a corrupción |
| `XVID` | `.avi` | Clásico, muy compatible |
| `MJPG` | `.avi` | Archivos grandes, muy rápido de codificar |
| `avc1` | `.mp4` | H.264, mejor compresión (puede requerir librerías extra) |

---

## Conceptos clave

- El contenedor (`.mkv`) y el codec (`XVID`) son conceptos distintos.
- `cv2.flip(frame, 1)` debe ir **antes** de `writer.write()` para que el espejo quede grabado.
- MKV es más resistente a corrupción que MP4 si el programa termina sin llamar `release()`.
- `XVID` + `.mkv` es una combinación confiable en Linux sin dependencias extra.
