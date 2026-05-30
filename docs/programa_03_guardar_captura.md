# Programa 03 — Guardar captura de pantalla

Muestra la cámara en tiempo real. Al presionar `s` guarda el frame actual como imagen PNG con nombre único basado en la fecha y hora. Presiona `q` para salir.

```python
import cv2
import time

cap = cv2.VideoCapture(0)

print("Presiona 's' para guardar una captura, 'q' para salir")

contador = 0

while True:
    ret, frame = cap.read()

    if not ret:
        break

    cv2.imshow("Camara", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("s"):
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"captura_{timestamp}_{contador}.png"
        cv2.imwrite(nombre_archivo, frame)
        print(f"Captura guardada: {nombre_archivo}")
        contador += 1

    elif key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
```

---

## Funciones nuevas en este programa

### `cv2.imwrite(filename, img)`

Guarda una imagen en disco.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `filename` | `str` | Ruta y nombre del archivo. La extensión determina el formato. |
| `img` | `numpy.ndarray` | Imagen a guardar. |

**Retorna:** `bool` — `True` si se guardó correctamente, `False` si hubo error.

```python
cv2.imwrite("foto.png", frame)       # PNG sin pérdida
cv2.imwrite("foto.jpg", frame)       # JPG con compresión
cv2.imwrite("foto.bmp", frame)       # BMP sin compresión
```

#### Formatos soportados

| Extensión | Formato | Compresión |
|---|---|---|
| `.png` | PNG | Sin pérdida |
| `.jpg` / `.jpeg` | JPEG | Con pérdida (recomendado para fotos) |
| `.bmp` | BMP | Sin compresión (archivos grandes) |
| `.tiff` | TIFF | Sin pérdida (uso profesional) |

#### Opciones de calidad (parámetro opcional)

```python
# JPG: calidad del 0 al 100 (default: 95)
cv2.imwrite("foto.jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 80])

# PNG: nivel de compresión del 0 al 9 (default: 3)
cv2.imwrite("foto.png", frame, [cv2.IMWRITE_PNG_COMPRESSION, 5])
```

---

### `time.strftime(formato)`

Genera una cadena de texto con la fecha y hora actual usando un formato específico.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `formato` | `str` | Plantilla con códigos de fecha/hora. |

**Retorna:** `str` con la fecha/hora formateada.

#### Códigos de formato más usados

| Código | Descripción | Ejemplo |
|---|---|---|
| `%Y` | Año con 4 dígitos | `2026` |
| `%m` | Mes con 2 dígitos | `05` |
| `%d` | Día con 2 dígitos | `30` |
| `%H` | Hora en formato 24h | `14` |
| `%M` | Minutos | `35` |
| `%S` | Segundos | `07` |

```python
time.strftime("%Y%m%d_%H%M%S")   # → "20260530_143507"
time.strftime("%d/%m/%Y")         # → "30/05/2026"
```

> **Por qué usarlo en nombres de archivo:** garantiza nombres únicos sin necesidad
> de verificar si el archivo ya existe. El formato `YYYYMMDD_HHMMSS` también permite
> ordenar los archivos cronológicamente por nombre.

---

### `ord(caracter)`

Convierte un carácter a su código ASCII entero.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `caracter` | `str` | Un solo carácter. |

**Retorna:** `int` — código ASCII del carácter.

```python
ord("s")   # → 115
ord("q")   # → 113
ord("a")   # → 97
```

> **Por qué se usa con `waitKey`:** `cv2.waitKey()` retorna el código ASCII de la
> tecla presionada. Para comparar con una letra legible se usa `ord()` en lugar
> de escribir el número directamente.

```python
# equivalente pero menos legible:
if key == 115:   # código ASCII de 's'
    ...

# legible:
if key == ord("s"):
    ...
```

---

## Patrón de múltiples teclas

En este programa se introducen **dos acciones por tecla** dentro del mismo loop.
La clave es guardar `waitKey` en una variable y luego comparar:

```python
key = cv2.waitKey(1) & 0xFF

if key == ord("s"):
    # acción 1
elif key == ord("q"):
    # acción 2
```

Esto permite agregar fácilmente más acciones sin llamar `waitKey` varias veces.

---

## Diferencia con programas anteriores

| Aspecto | Prog 01 | Prog 02 | Prog 03 |
|---|---|---|---|
| Guarda imágenes | No | No | Sí, con `s` |
| Nombre de archivo | — | — | Fecha + hora + contador |
| Múltiples teclas | No | No | Sí |
| Módulos nuevos | — | — | `time` |

---

## Conceptos clave

- `cv2.imwrite()` determina el formato por la extensión del archivo.
- Usar `time.strftime()` en el nombre evita sobreescribir capturas anteriores.
- El `contador` es una segunda garantía de unicidad si se toman varias fotos en el mismo segundo.
- Guardar `waitKey` en `key` permite manejar múltiples teclas limpiamente.
