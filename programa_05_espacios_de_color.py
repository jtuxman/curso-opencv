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

# Lista de los espacios de color disponibles para ciclar con 'm'
modos = ["BGR", "Gris", "HSV", "LAB"]

# Indice del modo activo. Empieza en 0 = "BGR" (imagen sin conversion)
modo_actual = 0

print("Presiona 'm' para cambiar modo, 'q' para salir")

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Obtenemos el nombre del modo activo usando el indice como posicion en la lista
    modo = modos[modo_actual]

    if modo == "Gris":
        # COLOR_BGR2GRAY convierte la imagen de 3 canales (BGR) a 1 canal (intensidad).
        # El resultado tiene forma (alto, ancho) en lugar de (alto, ancho, 3).
        # La conversion usa esta formula ponderada:
        #   L = 0.114*B + 0.587*G + 0.299*R
        # El verde tiene mas peso porque el ojo humano es mas sensible a el.
        salida = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Convertimos de vuelta a BGR (3 canales) aunque siga viendose gris.
        # Esto es necesario para que putText pueda dibujar texto en color
        # sin causar errores por incompatibilidad de canales.
        salida = cv2.cvtColor(salida, cv2.COLOR_GRAY2BGR)

    elif modo == "HSV":
        # COLOR_BGR2HSV convierte a Matiz-Saturacion-Valor:
        #   H (Hue/Matiz)       0-179  -> el color puro (rojo, verde, azul...)
        #   S (Saturation)      0-255  -> que tan "vivo" es el color (0=gris)
        #   V (Value/Brillo)    0-255  -> que tan claro u oscuro
        # HSV es el espacio preferido para detectar objetos por color
        # porque separa el color de la luminosidad, lo que lo hace
        # mas robusto ante cambios de iluminacion.
        salida = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    elif modo == "LAB":
        # COLOR_BGR2LAB convierte al espacio L*a*b* diseñado para
        # aproximarse a la percepcion humana del color:
        #   L -> Luminosidad  (0=negro, 255=blanco)
        #   a -> Verde(-) a Rojo(+)
        #   b -> Azul(-) a Amarillo(+)
        # Util para comparar colores tal como los percibe el ojo humano.
        salida = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)

    else:
        # Modo BGR: sin conversion, mostramos el frame original
        salida = frame

    # Mostramos el nombre del modo activo en la esquina superior izquierda
    cv2.putText(salida, f"Modo: {modo}  (M = cambiar)", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow("Espacios de color", salida)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("m"):
        # El operador % (modulo) hace que el indice vuelva a 0 al llegar al final.
        # Ejemplo con 4 modos: 0 -> 1 -> 2 -> 3 -> 0 -> 1 -> ...
        # Es el patron estandar para ciclar indefinidamente por una lista.
        modo_actual = (modo_actual + 1) % len(modos)

    elif key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
