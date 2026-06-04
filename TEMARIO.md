# Temario del curso OpenCV

Este documento organiza el curso de forma gradual. La meta es avanzar desde el
uso basico de una camara con OpenCV hasta deteccion de objetos, reconocimiento
de rostros y entrenamiento de modelos con objetos propios.

## Objetivo general

Aprender vision por computadora con OpenCV en Python mediante programas
pequenos, progresivos y bien documentados. Cada programa debe introducir pocos
conceptos nuevos, explicar las funciones usadas, mostrar errores comunes y dejar
una base clara para el siguiente tema.

## Ruta de aprendizaje

### Bloque 1: Fundamentos de camara y frames

| Programa | Estado | Objetivo |
|---|---|---|
| `programa_01_camara_basica.py` | Desarrollado | Abrir la camara, leer frames en tiempo real, mostrarlos en una ventana y cerrar correctamente los recursos. |
| `programa_02_propiedades_y_espejo.py` | Desarrollado | Leer propiedades de la camara como resolucion y FPS, y aplicar efecto espejo con `cv2.flip`. |
| `programa_03_guardar_captura.py` | Desarrollado | Guardar capturas de la camara en archivos de imagen usando `cv2.imwrite` y nombres con fecha/hora. |
| `programa_04_dibujar_en_frame.py` | Desarrollado | Dibujar rectangulos, circulos, lineas y texto sobre frames para crear anotaciones visuales. |

### Bloque 2: Procesamiento basico de imagen

| Programa | Estado | Objetivo |
|---|---|---|
| `programa_05_espacios_de_color.py` | Desarrollado | Convertir entre BGR, escala de grises, HSV y LAB para entender como cambia la representacion del color. |
| `programa_06_detectar_bordes.py` | Desarrollado | Aplicar suavizado gaussiano y detectar bordes con Canny. |
| `programa_09_redimensionar.py` | Desarrollado | Cambiar el tamano de un frame con distintos factores de escala e interpolaciones. |
| `programa_10_filtros_desenfoque.py` | Desarrollado | Comparar desenfoque gaussiano, mediano y bilateral, entendiendo para que sirve cada filtro. |

### Bloque 3: Captura y grabacion

| Programa | Estado | Objetivo |
|---|---|---|
| `programa_07_grabar_video.py` | Desarrollado | Grabar video en formato MP4 usando `cv2.VideoWriter`, controlando inicio y fin con teclado. |
| `programa_08_grabar_mkv.py` | Desarrollado | Grabar video MKV con codec XVID y aplicar efecto espejo antes de escribir el frame. |

### Bloque 4: Segmentacion de objetos simples

| Programa | Estado | Objetivo |
|---|---|---|
| `programa_11_umbralizacion.py` | Desarrollado | Separar pixeles claros/oscuros con umbralizacion binaria, adaptativa y Otsu. |
| `programa_12_segmentacion_por_color_hsv.py` | Desarrollado | Detectar objetos por color usando conversion a HSV y mascaras con `cv2.inRange`. |
| `programa_13_trackbars_hsv.py` | Desarrollado | Crear controles interactivos para calibrar rangos HSV en tiempo real. |
| `programa_14_morfologia.py` | Desarrollado | Limpiar mascaras con erosion, dilatacion, apertura y cierre. |
| `programa_15_contornos_y_bounding_boxes.py` | Desarrollado | Encontrar contornos, dibujar cajas delimitadoras, calcular area, centro y dimensiones. |

### Bloque 5: Primeros detectores hechos a mano

| Programa | Estado | Objetivo |
|---|---|---|
| `programa_16_detector_por_color_y_forma.py` | Propuesto | Combinar color, area y forma para detectar un objeto especifico sin usar aprendizaje automatico. |
| `programa_17_template_matching.py` | Propuesto | Buscar un objeto usando una imagen plantilla y `cv2.matchTemplate`. |
| `programa_18_deteccion_movimiento.py` | Propuesto | Detectar movimiento comparando frames consecutivos o contra un fondo de referencia. |
| `programa_19_tracking_basico.py` | Propuesto | Seguir objetos entre frames usando centros, distancias e identificadores simples. |

### Bloque 6: Deteccion y reconocimiento de rostros

| Programa | Estado | Objetivo |
|---|---|---|
| `programa_20_deteccion_rostros_haar.py` | Propuesto | Detectar rostros con clasificadores Haar preentrenados de OpenCV. |
| `programa_21_deteccion_rostro_ojos_sonrisa.py` | Propuesto | Extender la deteccion facial para localizar ojos y sonrisa con cascadas multiples. |
| `programa_22_crear_dataset_rostros.py` | Propuesto | Capturar y organizar imagenes etiquetadas de rostros para entrenamiento. |
| `programa_23_entrenar_reconocedor_lbph.py` | Propuesto | Entrenar un reconocedor facial LBPH usando imagenes propias. |
| `programa_24_reconocimiento_facial_en_vivo.py` | Propuesto | Usar el modelo entrenado para reconocer personas en vivo y manejar casos desconocidos. |

### Bloque 7: Deteccion de objetos con modelos

| Programa | Estado | Objetivo |
|---|---|---|
| `programa_25_intro_dnn_objetos.py` | Propuesto | Usar `cv2.dnn` con un modelo preentrenado para detectar objetos comunes. |
| `programa_26_crear_dataset_objetos_propios.py` | Propuesto | Capturar imagenes de objetos propios y organizarlas por etiqueta. |
| `programa_27_anotar_dataset_objetos.py` | Propuesto | Explicar cajas delimitadoras, etiquetas y formatos de anotacion para entrenamiento. |
| `programa_28_entrenar_modelo_objetos.py` | Propuesto | Entrenar un modelo de deteccion con objetos propios usando un flujo practico como YOLO. |
| `programa_29_usar_modelo_entrenado_camara.py` | Propuesto | Ejecutar inferencia en vivo con el modelo entrenado y mostrar cajas, etiquetas y confianza. |
| `programa_30_evaluacion_y_mejoras.py` | Propuesto | Evaluar errores, falsos positivos, falsos negativos, iluminacion, cantidad de datos y mejoras del dataset. |

## Criterios para cada programa

Cada programa nuevo debe mantener el estilo del curso:

- Codigo pequeno y ejecutable de forma independiente.
- Comentarios claros en el script.
- Documento equivalente en `docs/` con explicacion extendida.
- Explicacion de funciones nuevas, parametros importantes y errores comunes.
- Controles de teclado simples y consistentes.
- Validacion de camara, archivos y dependencias cuando aplique.
- Relacion explicita con los programas anteriores.

## Conceptos clave de progresion

- Primero se aprende a capturar y mostrar frames.
- Despues se aprende a transformar imagenes.
- Luego se separan objetos del fondo con mascaras.
- Mas adelante se miden regiones mediante contornos y cajas.
- Con esa base se construyen detectores simples.
- Finalmente se usan modelos entrenados para reconocer rostros y objetos.

## Notas de dependencias

Los programas iniciales usan `opencv-python`. Para reconocimiento facial con
LBPH sera necesario cambiar o ampliar la dependencia a `opencv-contrib-python`,
porque el modulo `cv2.face` pertenece a los modulos contrib de OpenCV.
