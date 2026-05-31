import cv2

cap = cv2.VideoCapture(0)

ancho_original = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
alto_original = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

escalas = [0.25, 0.5, 1.0, 1.5, 2.0]
indice = 2  # empieza en 1.0

print("Presiona '+' para agrandar, '-' para reducir, 'q' para salir")

while True:
    ret, frame = cap.read()

    if not ret:
        break

    escala = escalas[indice]
    nuevo_ancho = int(ancho_original * escala)
    nuevo_alto = int(alto_original * escala)

    if escala < 1.0:
        interpolacion = cv2.INTER_AREA
    else:
        interpolacion = cv2.INTER_LINEAR

    frame_redim = cv2.resize(frame, (nuevo_ancho, nuevo_alto), interpolation=interpolacion)

    etiqueta = f"Escala: {escala}x  ({nuevo_ancho}x{nuevo_alto})"
    cv2.putText(frame_redim, etiqueta, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    cv2.imshow("Redimensionar", frame_redim)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("+") and indice < len(escalas) - 1:
        indice += 1
    elif key == ord("-") and indice > 0:
        indice -= 1
    elif key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
