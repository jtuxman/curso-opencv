import cv2

cap = cv2.VideoCapture(0)

modos = ["BGR", "Gris", "HSV", "LAB"]
modo_actual = 0

print("Presiona 'm' para cambiar modo, 'q' para salir")

while True:
    ret, frame = cap.read()

    if not ret:
        break

    modo = modos[modo_actual]

    if modo == "Gris":
        salida = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        salida = cv2.cvtColor(salida, cv2.COLOR_GRAY2BGR)
    elif modo == "HSV":
        salida = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    elif modo == "LAB":
        salida = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    else:
        salida = frame

    cv2.putText(salida, f"Modo: {modo}  (M = cambiar)", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow("Espacios de color", salida)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("m"):
        modo_actual = (modo_actual + 1) % len(modos)

    elif key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
