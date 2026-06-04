try:
    import cv2
except ModuleNotFoundError:
    raise SystemExit(
        "No se encontro OpenCV (cv2). Instala las dependencias con:\n"
        "  python -m pip install -r requirements.txt"
    )

# VideoCapture(0) abre la camara conectada al sistema.
# El argumento 0 indica el indice del dispositivo:
#   0 = camara por defecto (integrada o la primera detectada)
#   1, 2, 3... = camaras adicionales en orden de deteccion
# Tambien acepta una ruta de archivo: VideoCapture("video.mp4")
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise SystemExit(
        "No se pudo abrir la camara. Verifica que este conectada, "
        "que no la use otro programa y que tengas permisos sobre el dispositivo."
    )

# El loop se ejecuta indefinidamente hasta que el usuario presione 'q'
# o la camara deje de enviar frames (desconexion, fin de archivo, etc.)
while True:

    # cap.read() captura el siguiente frame de la camara.
    # Retorna dos valores:
    #   ret   -> bool: True si el frame se leyó correctamente, False si hubo error
    #   frame -> ndarray de NumPy con forma (alto, ancho, 3) en formato BGR
    # Si la camara esta desconectada o el video termino, ret sera False
    ret, frame = cap.read()

    # Si ret es False no hay frame valido; salimos del loop para evitar errores
    if not ret:
        print("No se pudo leer el frame")
        break

    # imshow muestra el frame en una ventana con el titulo indicado.
    # Si la ventana no existe la crea automaticamente.
    # El frame debe ser un array NumPy de tipo uint8 (valores 0-255)
    cv2.imshow("Camara", frame)

    # waitKey(1) espera 1 milisegundo antes de continuar.
    # Es obligatorio en el loop: sin esta llamada la ventana no se refresca
    # y el programa se congela mostrando solo el primer frame.
    #
    # Retorna el codigo ASCII de la tecla presionada, o -1 si no se presiono ninguna.
    #
    # El operador & 0xFF aplica una mascara de bits para quedarse solo
    # con los 8 bits menos significativos. Esto es necesario porque en
    # algunos sistemas waitKey retorna valores de 32 bits donde los bits
    # superiores contienen informacion extra del sistema operativo.
    # ord("q") convierte el caracter 'q' a su codigo ASCII (113)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# release() libera el dispositivo de camara y cierra la conexion.
# Sin esta llamada la camara puede quedar bloqueada para otras aplicaciones
# hasta que el proceso de Python termine completamente.
cap.release()

# destroyAllWindows() cierra todas las ventanas abiertas por OpenCV.
# Si no se llama, las ventanas pueden quedar abiertas (especialmente en Windows).
cv2.destroyAllWindows()
