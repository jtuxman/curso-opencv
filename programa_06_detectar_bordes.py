import cv2

cap = cv2.VideoCapture(0)

umbral1 = 50
umbral2 = 150

print("Presiona 'm' para alternar original/bordes, 'q' para salir")

mostrar_bordes = True

while True:
    ret, frame = cap.read()

    if not ret:
        break

    gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gris = cv2.GaussianBlur(gris, (5, 5), 0)
    bordes = cv2.Canny(gris, umbral1, umbral2)

    if mostrar_bordes:
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
        mostrar_bordes = not mostrar_bordes
    elif key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
