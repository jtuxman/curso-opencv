# Curso OpenCV

Ejemplos practicos de OpenCV en Python usando una camara web. Cada programa
tiene su explicacion extendida en la carpeta `docs/`.

El plan completo del curso esta en `TEMARIO.md`.

## Instalacion

El error:

```bash
ModuleNotFoundError: No module named 'cv2'
```

significa que OpenCV no esta instalado en el entorno de Python con el que estas
ejecutando los programas. Instala las dependencias asi:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Despues ejecuta cualquier programa con el entorno activado:

```bash
python programa_01_camara_basica.py
```

Para salir de los programas, presiona `q` en la ventana de OpenCV.

## Requisitos

- Python 3.9 o superior.
- Una camara web disponible.
- En Linux, acceso al dispositivo de camara, normalmente `/dev/video0`.

Si la camara no abre, prueba revisar que otro programa no la este usando y que
tu usuario tenga permisos sobre el dispositivo:

```bash
ls -l /dev/video*
```

## Problemas comunes en Linux

Si `python3 -m venv .venv` falla, instala el paquete de entornos virtuales:

```bash
sudo apt install python3-venv
```

Si despues de instalar OpenCV aparece un error relacionado con `libGL.so.1`,
instala la libreria grafica del sistema:

```bash
sudo apt install libgl1
```

## Programas

| Archivo | Tema |
|---|---|
| `programa_01_camara_basica.py` | Abrir la camara y mostrar video en vivo |
| `programa_02_propiedades_y_espejo.py` | Leer propiedades y aplicar efecto espejo |
| `programa_03_guardar_captura.py` | Guardar capturas con `s` |
| `programa_04_dibujar_en_frame.py` | Dibujar figuras y texto sobre el frame |
| `programa_05_espacios_de_color.py` | Cambiar entre BGR, gris, HSV y LAB |
| `programa_06_detectar_bordes.py` | Detectar bordes con Canny |
| `programa_07_grabar_video.py` | Grabar video MP4 |
| `programa_08_grabar_mkv.py` | Grabar video MKV con efecto espejo |
| `programa_09_redimensionar.py` | Redimensionar el frame |
| `programa_10_filtros_desenfoque.py` | Comparar filtros de desenfoque |
| `programa_11_umbralizacion.py` | Comparar umbralizacion binaria, adaptativa y Otsu |
| `programa_12_segmentacion_por_color_hsv.py` | Detectar objetos por color usando HSV |
| `programa_13_trackbars_hsv.py` | Calibrar rangos HSV con controles interactivos |
| `programa_14_morfologia.py` | Limpiar mascaras con erosion, dilatacion, apertura y cierre |
| `programa_15_contornos_y_bounding_boxes.py` | Encontrar contornos, cajas, areas y centros |

## Archivos generados

Algunos programas crean archivos como `captura_*.png`, `video_*.mp4` o
`video_*.mkv`. Estan ignorados por Git para no subir capturas o grabaciones al
repositorio.
