try:
    import cv2
except ModuleNotFoundError:
    raise SystemExit(
        "No se encontro OpenCV (cv2). Instala las dependencias con:\n"
        "  python -m pip install -r requirements.txt"
    )

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise SystemExit(
        "No se pudo abrir la camara. Verifica que este conectada, "
        "que no la use otro programa y que tengas permisos sobre el dispositivo."
    )

# Este programa conecta tres ideas ya vistas:
#   1. segmentacion por color HSV       -> programas 12 y 13
#   2. limpieza de mascara con morfologia -> programa 14
#   3. medicion de regiones detectadas    -> este programa
#
# El resultado sera una lista de "objetos candidatos". Cada candidato
# tendra contorno, caja delimitadora, area, centro y dimensiones.

colores = {
    "Rojo": [
        ((0, 80, 80), (10, 255, 255)),
        ((170, 80, 80), (179, 255, 255)),
    ],
    "Verde": [
        ((35, 60, 60), (85, 255, 255)),
    ],
    "Azul": [
        ((90, 60, 60), (130, 255, 255)),
    ],
    "Amarillo": [
        ((20, 60, 60), (35, 255, 255)),
    ],
    "Naranja": [
        ((10, 80, 80), (25, 255, 255)),
    ],
}

nombres_colores = list(colores.keys())
indice_color = 0

vistas = ["Deteccion", "Mascara", "Contornos", "Original"]
indice_vista = 0

# RETR_EXTERNAL detecta solo contornos externos. Es lo mas comun cuando
# queremos una caja por objeto y no nos interesan huecos internos.
# RETR_LIST detecta todos los contornos sin organizar jerarquias.
modos_recuperacion = [
    ("Externos", cv2.RETR_EXTERNAL),
    ("Todos", cv2.RETR_LIST),
]
indice_recuperacion = 0

# Area minima para aceptar un contorno como objeto real.
# Si se deja muy baja, aparecera ruido. Si se deja muy alta, objetos pequenos
# seran ignorados. Se puede ajustar con '+' y '-'.
area_minima = 1000
paso_area = 250

# Kernel fijo para limpiar la mascara antes de buscar contornos.
# En este programa el foco es medir objetos, no calibrar morfologia; por eso
# usamos una limpieza razonable y dejamos el ajuste fino para el programa 14.
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))


def crear_mascara_color(hsv, color_objetivo):
    """Crea una mascara binaria para el color seleccionado."""
    mascara = None

    for bajo, alto in colores[color_objetivo]:
        mascara_rango = cv2.inRange(hsv, bajo, alto)

        if mascara is None:
            mascara = mascara_rango
        else:
            # Esto permite combinar los dos rangos del rojo.
            mascara = cv2.bitwise_or(mascara, mascara_rango)

    return mascara


def limpiar_mascara(mascara):
    """Reduce ruido y rellena huecos pequenos antes de buscar contornos."""
    # Apertura: elimina puntos blancos pequenos del fondo.
    limpia = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, kernel, iterations=1)

    # Cierre: rellena huecos negros pequenos dentro del objeto.
    limpia = cv2.morphologyEx(limpia, cv2.MORPH_CLOSE, kernel, iterations=1)

    return limpia


def centroide_desde_momentos(contorno, x, y, w, h):
    """Calcula el centro del contorno usando momentos; usa la caja como respaldo."""
    momentos = cv2.moments(contorno)

    if momentos["m00"] != 0:
        # m00 representa el area del contorno.
        # m10/m00 y m01/m00 calculan el centroide geometrico.
        cx = int(momentos["m10"] / momentos["m00"])
        cy = int(momentos["m01"] / momentos["m00"])
    else:
        # Si el area es 0, evitamos division entre cero.
        # Como respaldo usamos el centro de la caja delimitadora.
        cx = x + w // 2
        cy = y + h // 2

    return cx, cy


def analizar_contornos(contornos, area_min):
    """Filtra contornos pequenos y calcula mediciones de cada objeto."""
    objetos = []

    for contorno in contornos:
        area = cv2.contourArea(contorno)

        # Ignoramos regiones pequenas para reducir ruido.
        # El area se mide en pixeles cuadrados, no en centimetros.
        if area < area_min:
            continue

        # boundingRect devuelve una caja recta alineada con los ejes X/Y.
        # x,y es la esquina superior izquierda; w,h son ancho y alto.
        x, y, w, h = cv2.boundingRect(contorno)
        cx, cy = centroide_desde_momentos(contorno, x, y, w, h)

        objetos.append({
            "contorno": contorno,
            "area": area,
            "x": x,
            "y": y,
            "w": w,
            "h": h,
            "cx": cx,
            "cy": cy,
        })

    # Ordenamos de mayor a menor area para que el objeto principal quede primero.
    objetos.sort(key=lambda objeto: objeto["area"], reverse=True)

    return objetos


def dibujar_objetos(frame, objetos):
    """Dibuja contorno, caja, centro y texto de cada objeto detectado."""
    salida = frame.copy()

    for indice, objeto in enumerate(objetos, start=1):
        contorno = objeto["contorno"]
        area = objeto["area"]
        x = objeto["x"]
        y = objeto["y"]
        w = objeto["w"]
        h = objeto["h"]
        cx = objeto["cx"]
        cy = objeto["cy"]

        # El contorno muestra la forma real detectada.
        cv2.drawContours(salida, [contorno], -1, (0, 255, 255), 2)

        # La caja delimitadora simplifica esa forma a un rectangulo.
        # Esta caja sera la base para detectores posteriores.
        cv2.rectangle(salida, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # El centroide indica el centro geometrico de la region.
        # Es util para tracking, apuntar a un objeto o calcular movimiento.
        cv2.circle(salida, (cx, cy), 5, (0, 0, 255), -1)

        texto_1 = f"#{indice} area={int(area)}"
        texto_2 = f"centro=({cx},{cy}) tam={w}x{h}"

        cv2.putText(salida, texto_1, (x, max(20, y - 25)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 2)
        cv2.putText(salida, texto_2, (x, max(40, y - 5)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.50, (0, 255, 0), 2)

    return salida


print("Presiona 'c' para cambiar color")
print("Presiona 'v' para cambiar vista")
print("Presiona 'r' para cambiar modo de recuperacion de contornos")
print("Presiona '+' o '-' para ajustar area minima")
print("Presiona 'q' para salir")

while True:
    ret, frame = cap.read()

    if not ret:
        break

    color_objetivo = nombres_colores[indice_color]
    vista = vistas[indice_vista]
    nombre_recuperacion, modo_recuperacion = modos_recuperacion[indice_recuperacion]

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mascara_original = crear_mascara_color(hsv, color_objetivo)
    mascara_limpia = limpiar_mascara(mascara_original)

    # findContours busca regiones blancas conectadas en una mascara binaria.
    # Importante: el objeto de interes debe estar en blanco y el fondo en negro.
    contornos, jerarquia = cv2.findContours(
        mascara_limpia, modo_recuperacion, cv2.CHAIN_APPROX_SIMPLE
    )

    objetos = analizar_contornos(contornos, area_minima)
    deteccion = dibujar_objetos(frame, objetos)

    if vista == "Deteccion":
        salida = deteccion

    elif vista == "Mascara":
        salida = cv2.cvtColor(mascara_limpia, cv2.COLOR_GRAY2BGR)

    elif vista == "Contornos":
        salida = frame.copy()
        cv2.drawContours(salida, contornos, -1, (0, 255, 255), 2)

    else:
        salida = frame

    etiqueta = (
        f"Vista: {vista}  Color: {color_objetivo}  "
        f"Contornos: {len(contornos)}  Objetos: {len(objetos)}"
    )
    filtro = f"Area minima: {area_minima}  Recuperacion: {nombre_recuperacion}"

    cv2.putText(salida, etiqueta, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 2)
    cv2.putText(salida, filtro, (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 2)
    cv2.putText(salida, "V=vista  C=color  R=recuperacion  +/-=area  Q=salir",
                (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 2)

    cv2.imshow("Contornos y bounding boxes", salida)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("v"):
        indice_vista = (indice_vista + 1) % len(vistas)

    elif key == ord("c"):
        indice_color = (indice_color + 1) % len(nombres_colores)

    elif key == ord("r"):
        indice_recuperacion = (indice_recuperacion + 1) % len(modos_recuperacion)

    elif key == ord("+"):
        area_minima += paso_area

    elif key == ord("-"):
        area_minima = max(0, area_minima - paso_area)

    elif key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
