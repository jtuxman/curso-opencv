try:
    import cv2
except ModuleNotFoundError:
    raise SystemExit(
        "No se encontro OpenCV (cv2). Instala las dependencias con:\n"
        "  python -m pip install -r requirements.txt"
    )

# Abre la camara con indice 0 (camara por defecto)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise SystemExit(
        "No se pudo abrir la camara. Verifica que este conectada, "
        "que no la use otro programa y que tengas permisos sobre el dispositivo."
    )

# cap.get(propId) lee una propiedad del dispositivo de captura.
# Siempre retorna float, por eso se convierte a int para mostrar valores enteros.
# CAP_PROP_FRAME_WIDTH  -> ancho del frame en pixeles
# CAP_PROP_FRAME_HEIGHT -> alto del frame en pixeles
# CAP_PROP_FPS          -> frames por segundo reportados por la camara
ancho = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
alto = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
fps = cap.get(cv2.CAP_PROP_FPS)

# Se imprimen ANTES del loop porque estas propiedades son fijas
# durante toda la sesion; no cambian frame a frame
print(f"Resolución: {int(ancho)} x {int(alto)}")
print(f"FPS: {fps}")

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # cv2.flip(src, flipCode) voltea la imagen segun el eje indicado:
    #   flipCode =  1 -> horizontal (espejo izquierda/derecha) <- usamos este
    #   flipCode =  0 -> vertical   (boca abajo)
    #   flipCode = -1 -> ambos ejes (rotacion de 180 grados)
    #
    # Retorna un nuevo array; NO modifica frame en su lugar.
    # El efecto espejo hace que los movimientos se vean naturales,
    # igual que cuando uno se mira en un espejo fisico.
    frame_espejo = cv2.flip(frame, 1)

    # Mostramos el frame volteado, no el original
    cv2.imshow("Camara espejo", frame_espejo)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
