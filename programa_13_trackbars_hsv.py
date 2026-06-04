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


def nada(valor):
    # createTrackbar exige una funcion callback.
    # En este programa no necesitamos reaccionar inmediatamente al movimiento;
    # leemos el valor de cada trackbar en cada vuelta del loop principal.
    pass


ventana_controles = "Controles HSV"
cv2.namedWindow(ventana_controles)

# Trackbars para definir el rango HSV.
# H va de 0 a 179 en OpenCV, no de 0 a 360.
# S y V van de 0 a 255.
#
# Cada trackbar permite cambiar un limite sin editar el codigo.
# En vez de escribir nuevos valores y reiniciar el programa, el alumno
# puede mover el control y ver el efecto inmediatamente en la mascara.
cv2.createTrackbar("H min", ventana_controles, 170, 179, nada)
cv2.createTrackbar("H max", ventana_controles, 10, 179, nada)
cv2.createTrackbar("S min", ventana_controles, 80, 255, nada)
cv2.createTrackbar("S max", ventana_controles, 255, 255, nada)
cv2.createTrackbar("V min", ventana_controles, 80, 255, nada)
cv2.createTrackbar("V max", ventana_controles, 255, 255, nada)

# Presets de partida. No son valores perfectos; sirven para aproximarse
# rapidamente y luego ajustar a mano segun camara, luz y objeto.
# En rojo usamos H min > H max para representar un rango circular:
# 170..179 OR 0..10.
#
# Estos presets son equivalentes a los rangos fijos del programa 12, pero
# ahora se cargan en controles editables. Despues de mover un trackbar,
# el preset solo indica el punto de partida, no necesariamente el valor actual.
presets = {
    "Rojo": (170, 10, 80, 255, 80, 255),
    "Verde": (35, 85, 60, 255, 60, 255),
    "Azul": (90, 130, 60, 255, 60, 255),
    "Amarillo": (20, 35, 60, 255, 60, 255),
    "Naranja": (10, 25, 80, 255, 80, 255),
}

nombres_presets = list(presets.keys())
indice_preset = 0

modos = ["Mascara", "Resultado", "Original", "Matiz"]
indice_modo = 0


def aplicar_preset(nombre):
    # Carga en los trackbars los valores iniciales del preset.
    # setTrackbarPos actualiza visualmente el control y tambien cambia
    # el valor que getTrackbarPos devolvera en el loop principal.
    h_min, h_max, s_min, s_max, v_min, v_max = presets[nombre]
    cv2.setTrackbarPos("H min", ventana_controles, h_min)
    cv2.setTrackbarPos("H max", ventana_controles, h_max)
    cv2.setTrackbarPos("S min", ventana_controles, s_min)
    cv2.setTrackbarPos("S max", ventana_controles, s_max)
    cv2.setTrackbarPos("V min", ventana_controles, v_min)
    cv2.setTrackbarPos("V max", ventana_controles, v_max)


def leer_rango_hsv():
    # Leemos los valores actuales de la interfaz en cada frame.
    # Esto es lo que hace que la calibracion sea "en vivo":
    # mover una barra afecta la mascara en la siguiente iteracion del loop.
    h_min = cv2.getTrackbarPos("H min", ventana_controles)
    h_max = cv2.getTrackbarPos("H max", ventana_controles)
    s_min = cv2.getTrackbarPos("S min", ventana_controles)
    s_max = cv2.getTrackbarPos("S max", ventana_controles)
    v_min = cv2.getTrackbarPos("V min", ventana_controles)
    v_max = cv2.getTrackbarPos("V max", ventana_controles)

    # Para S y V no existe una escala circular, asi que si el usuario
    # deja min > max, ordenamos los valores para evitar una mascara vacia.
    s_bajo = min(s_min, s_max)
    s_alto = max(s_min, s_max)
    v_bajo = min(v_min, v_max)
    v_alto = max(v_min, v_max)

    return h_min, h_max, s_bajo, s_alto, v_bajo, v_alto


def crear_mascara_hsv(hsv, h_min, h_max, s_min, s_max, v_min, v_max):
    # Esta funcion encapsula el detalle mas importante del programa:
    # H puede comportarse como rango normal o como rango circular.
    #
    # Rango normal:
    #   H min=35, H max=85  -> detectar H entre 35 y 85.
    #
    # Rango circular:
    #   H min=170, H max=10 -> detectar H entre 170..179 o 0..10.
    if h_min <= h_max:
        # Rango normal:
        # H min ... H max
        bajo = (h_min, s_min, v_min)
        alto = (h_max, s_max, v_max)
        mascara = cv2.inRange(hsv, bajo, alto)
        descripcion = f"({bajo}) - ({alto})"
    else:
        # Rango circular:
        # H min ... 179  OR  0 ... H max
        # Esto es especialmente util para rojo.
        # Sin esta regla, calibrar rojo requeriria dos pares de trackbars
        # para dos mascaras separadas.
        bajo_1 = (h_min, s_min, v_min)
        alto_1 = (179, s_max, v_max)
        bajo_2 = (0, s_min, v_min)
        alto_2 = (h_max, s_max, v_max)

        mascara_1 = cv2.inRange(hsv, bajo_1, alto_1)
        mascara_2 = cv2.inRange(hsv, bajo_2, alto_2)
        mascara = cv2.bitwise_or(mascara_1, mascara_2)
        descripcion = f"({bajo_1})-({alto_1}) OR ({bajo_2})-({alto_2})"

    return mascara, descripcion


aplicar_preset(nombres_presets[indice_preset])

print("Presiona 'c' para cambiar preset")
print("Presiona 'm' para cambiar vista")
print("Presiona 'p' para imprimir el rango HSV actual")
print("Presiona 'q' para salir")

while True:
    ret, frame = cap.read()

    if not ret:
        break

    preset_actual = nombres_presets[indice_preset]
    modo = modos[indice_modo]

    # El frame llega en BGR, pero los controles estan pensados para HSV.
    # Primero convertimos, luego aplicamos el rango leido de los trackbars.
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h_min, h_max, s_min, s_max, v_min, v_max = leer_rango_hsv()
    mascara, descripcion_rango = crear_mascara_hsv(
        hsv, h_min, h_max, s_min, s_max, v_min, v_max
    )

    # El resultado permite revisar si la mascara esta seleccionando
    # exactamente el objeto. La mascara puede parecer correcta pero el
    # resultado revela reflejos o regiones no deseadas.
    resultado = cv2.bitwise_and(frame, frame, mask=mascara)

    # Vista didactica del canal H: ayuda a comprender que "color" esta viendo
    # OpenCV, independientemente del brillo original.
    hsv_matiz = hsv.copy()
    hsv_matiz[:, :, 1] = 255
    hsv_matiz[:, :, 2] = 255
    visual_matiz = cv2.cvtColor(hsv_matiz, cv2.COLOR_HSV2BGR)

    # Esta medicion sirve como indicador rapido de calibracion:
    # - 0%: no detecta nada.
    # - porcentaje muy alto: el rango probablemente incluye fondo.
    # - porcentaje estable: el objeto se detecta de forma consistente.
    pixeles_detectados = cv2.countNonZero(mascara)
    total_pixeles = mascara.shape[0] * mascara.shape[1]
    porcentaje = (pixeles_detectados / total_pixeles) * 100

    if modo == "Mascara":
        salida = cv2.cvtColor(mascara, cv2.COLOR_GRAY2BGR)
    elif modo == "Resultado":
        salida = resultado
    elif modo == "Original":
        salida = frame
    else:
        salida = visual_matiz

    etiqueta = (
        f"Vista: {modo}  Base: {preset_actual}  "
        f"H:{h_min}-{h_max} S:{s_min}-{s_max} V:{v_min}-{v_max}"
    )
    medicion = f"Pixeles detectados: {pixeles_detectados} ({porcentaje:.1f}%)"

    cv2.putText(salida, etiqueta, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 2)
    cv2.putText(salida, medicion, (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 2)
    cv2.putText(salida, "M=vista  C=preset  P=imprimir  Q=salir", (10, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 2)

    cv2.imshow("Calibracion HSV", salida)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("m"):
        # Cambia la forma de inspeccionar la calibracion:
        # Mascara, Resultado, Original o Matiz.
        indice_modo = (indice_modo + 1) % len(modos)

    elif key == ord("c"):
        # Carga otro preset como punto de partida.
        # Los ajustes manuales anteriores se reemplazan por los del nuevo color.
        indice_preset = (indice_preset + 1) % len(nombres_presets)
        aplicar_preset(nombres_presets[indice_preset])

    elif key == ord("p"):
        # Imprime los valores para copiarlos a otro programa.
        # Esta es la forma de pasar de calibracion interactiva a codigo fijo.
        print(f"Color base: {preset_actual}")
        print(f"Rango HSV actual: {descripcion_rango}")
        print(
            "Valores: "
            f"h_min={h_min}, h_max={h_max}, "
            f"s_min={s_min}, s_max={s_max}, "
            f"v_min={v_min}, v_max={v_max}"
        )

    elif key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
