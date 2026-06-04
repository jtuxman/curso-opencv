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

# Umbrales del algoritmo Canny para clasificar pixeles como borde o no:
#   umbral1 (bajo)  -> pixeles con gradiente menor son descartados
#   umbral2 (alto)  -> pixeles con gradiente mayor son bordes seguros
#   Los pixeles entre ambos umbrales se incluyen solo si tocan un borde seguro
# Regla practica: umbral2 ≈ 3 * umbral1
umbral1 = 50
umbral2 = 150

print("Presiona 'm' para alternar original/bordes, 'q' para salir")

# Variable booleana que controla si se muestra la imagen con bordes o la original
mostrar_bordes = True

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # PASO 1: Convertir a escala de grises.
    # Canny solo acepta imagenes de 1 canal; si se le pasa BGR produce error.
    gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # PASO 2: Suavizar con filtro gaussiano para eliminar ruido.
    # Sin este paso, el ruido natural de la camara (variaciones aleatorias
    # de brillo pixel a pixel) generaria cientos de falsos bordes.
    # Kernel (5,5): vecindad de 5x5 pixeles alrededor de cada punto.
    # El tercer argumento (0) indica que sigmaX se calcula automaticamente
    # a partir del tamanio del kernel.
    gris = cv2.GaussianBlur(gris, (5, 5), 0)

    # PASO 3: Detectar bordes con Canny.
    # El algoritmo calcula el gradiente (cambio de intensidad) en cada pixel.
    # Pixeles con gradiente alto (cambio brusco) son marcados como bordes (255=blanco).
    # El resto queda en negro (0).
    # La imagen resultante es binaria: solo 0 o 255.
    bordes = cv2.Canny(gris, umbral1, umbral2)

    if mostrar_bordes:
        # Convertimos bordes (1 canal) a BGR (3 canales) para poder
        # superponer texto en color sin errores de incompatibilidad.
        salida = cv2.cvtColor(bordes, cv2.COLOR_GRAY2BGR)
        etiqueta = f"Canny  umbral1={umbral1}  umbral2={umbral2}"
    else:
        salida = frame
        etiqueta = "Original"

    cv2.putText(salida, etiqueta, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("Deteccion de bordes", salida)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("m"):
        # El operador not invierte el valor booleano:
        # True -> False, False -> True
        # Patron simple para alternar entre dos estados (on/off)
        mostrar_bordes = not mostrar_bordes
    elif key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
