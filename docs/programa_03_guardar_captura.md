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

Guarda una imagen en disco. El formato se determina automáticamente por la extensión del archivo.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `filename` | `str` | Ruta y nombre del archivo incluyendo la extensión. |
| `img` | `numpy.ndarray` | Imagen a guardar en formato BGR (como la entrega `cap.read()`). |

**Retorna:** `bool` — `True` si se guardó correctamente, `False` si hubo error.

**Ejemplos:**

```python
# Guardar en diferentes formatos:
cv2.imwrite("foto.png", frame)       # PNG — sin pérdida de calidad
cv2.imwrite("foto.jpg", frame)       # JPG — compresión con pérdida
cv2.imwrite("foto.bmp", frame)       # BMP — sin compresión, archivos grandes
cv2.imwrite("foto.tiff", frame)      # TIFF — sin pérdida, uso profesional

# Guardar con ruta específica:
cv2.imwrite("/home/usuario/fotos/captura.png", frame)
cv2.imwrite("capturas/foto_001.jpg", frame)  # la carpeta debe existir

# Controlar la calidad del JPG (0=mínima calidad/menor tamaño, 100=máxima):
cv2.imwrite("foto.jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 95])   # alta calidad
cv2.imwrite("foto.jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 50])   # mitad de calidad
cv2.imwrite("foto.jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 20])   # baja calidad, archivo pequeño

# Controlar la compresión del PNG (0=sin compresión/archivo grande, 9=máxima compresión):
cv2.imwrite("foto.png", frame, [cv2.IMWRITE_PNG_COMPRESSION, 0])  # más rápido, más grande
cv2.imwrite("foto.png", frame, [cv2.IMWRITE_PNG_COMPRESSION, 9])  # más lento, más pequeño

# Verificar si se guardó correctamente:
guardado = cv2.imwrite("foto.png", frame)
if not guardado:
    print("Error: no se pudo guardar la imagen")
    # Causas comunes: la carpeta no existe, sin permisos de escritura,
    # extensión no soportada, o ruta inválida
```

#### Comparación de formatos

| Formato | Pérdida | Tamaño | Cuándo usar |
|---|---|---|---|
| `.png` | Sin pérdida | Mediano | Capturas, imágenes para procesar |
| `.jpg` | Con pérdida | Pequeño | Fotos para compartir o almacenar |
| `.bmp` | Sin pérdida | Grande | Compatibilidad máxima, edición |
| `.tiff` | Sin pérdida | Grande | Fotografía profesional |

---

### `time.strftime(formato)`

Genera una cadena de texto con la fecha y hora actual según un formato definido.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `formato` | `str` | Plantilla con códigos que se reemplazan por los valores de fecha/hora. |

**Retorna:** `str` — fecha y hora formateada como texto.

**Ejemplos:**

```python
import time

# Formatos comunes:
time.strftime("%Y%m%d_%H%M%S")    # → "20260530_143507"  (para nombres de archivo)
time.strftime("%d/%m/%Y")          # → "30/05/2026"       (fecha legible en español)
time.strftime("%Y-%m-%d")          # → "2026-05-30"       (formato ISO 8601)
time.strftime("%H:%M:%S")          # → "14:35:07"         (solo hora)
time.strftime("%d de %B de %Y")    # → "30 de May de 2026" (con nombre del mes en inglés)

# En nombres de archivo, evitar espacios y caracteres especiales:
# BIEN:   "captura_20260530_143507.png"   (usa _ y sin espacios)
# MAL:    "captura 30/05/2026 14:35.png"  (espacios y / causan problemas)

# Aplicado en el programa:
timestamp = time.strftime("%Y%m%d_%H%M%S")
nombre = f"captura_{timestamp}_0.png"
# → "captura_20260530_143507_0.png"
```

#### Códigos de formato

| Código | Descripción | Ejemplo |
|---|---|---|
| `%Y` | Año con 4 dígitos | `2026` |
| `%m` | Mes con 2 dígitos | `05` |
| `%d` | Día con 2 dígitos | `30` |
| `%H` | Hora formato 24h | `14` |
| `%M` | Minutos | `35` |
| `%S` | Segundos | `07` |
| `%A` | Nombre del día (inglés) | `Friday` |
| `%B` | Nombre del mes (inglés) | `May` |

---

### `ord(caracter)`

Convierte un carácter a su código ASCII entero.

| Parámetro | Tipo | Descripción |
|---|---|---|
| `caracter` | `str` | Un solo carácter. |

**Retorna:** `int` — código ASCII del carácter.

**Ejemplos:**

```python
ord("q")   # → 113
ord("s")   # → 115
ord("a")   # → 97
ord("A")   # → 65  (mayúsculas tienen código diferente)
ord(" ")   # → 32  (espacio)
ord("0")   # → 48  (el carácter "0", no el número 0)

# Se usa para comparar la tecla presionada de forma legible:
key = cv2.waitKey(1) & 0xFF

# Sin ord() (difícil de leer):
if key == 115:   # ¿qué tecla es 115? hay que buscarlo
    cv2.imwrite("foto.png", frame)

# Con ord() (legible):
if key == ord("s"):   # queda claro que es la tecla 's'
    cv2.imwrite("foto.png", frame)

# Detectar múltiples teclas:
if key == ord("s"):
    cv2.imwrite("foto.png", frame)
elif key == ord("f"):
    frame = cv2.flip(frame, 1)
elif key == ord("g"):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
elif key == ord("q"):
    break
```

---

## Patrón de múltiples teclas

En este programa se introduce el patrón de guardar `waitKey` en una variable
para manejar más de una tecla:

```python
# Patrón CORRECTO: una sola llamada a waitKey, guardada en variable
key = cv2.waitKey(1) & 0xFF

if key == ord("s"):
    # guardar
elif key == ord("q"):
    # salir

# Patrón INCORRECTO: llamar waitKey varias veces
if cv2.waitKey(1) & 0xFF == ord("s"):   # primera espera de 1ms
    # guardar
if cv2.waitKey(1) & 0xFF == ord("q"):   # segunda espera de 1ms — duplica el delay
    # salir
# Esto hace que el loop sea 2ms más lento en cada iteración
# y puede perder pulsaciones de teclas
```

---

## Diferencia con programas anteriores

| Aspecto | Prog 01-02 | Prog 03 |
|---|---|---|
| Guarda imágenes | No | Sí, con tecla `s` |
| Nombre de archivo | — | Fecha + hora + contador |
| Múltiples teclas | No | Sí, patrón con variable `key` |
| Módulos nuevos | — | `time` |

---

## Conceptos clave

- `cv2.imwrite()` determina el formato por la extensión del archivo.
- `time.strftime()` en el nombre evita sobreescribir capturas anteriores.
- El `contador` garantiza unicidad si se toman varias fotos en el mismo segundo.
- Guardar `waitKey` en `key` evita llamarlo dos veces y permite manejar múltiples teclas.
- `imwrite` retorna `False` silenciosamente si falla — verificar el retorno en producción.
