import cv2

cap = cv2.VideoCapture(0)

filtros = ["Sin filtro", "Gaussiano", "Mediano", "Bilateral"]
indice = 0

print("Presiona 'm' para cambiar filtro, 'q' para salir")

while True:
    ret, frame = cap.read()

    if not ret:
        break

    filtro = filtros[indice]

    if filtro == "Gaussiano":
        salida = cv2.GaussianBlur(frame, (15, 15), 0)
    elif filtro == "Mediano":
        salida = cv2.medianBlur(frame, 15)
    elif filtro == "Bilateral":
        salida = cv2.bilateralFilter(frame, 9, 75, 75)
    else:
        salida = frame

    cv2.putText(salida, f"Filtro: {filtro}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("Filtros de desenfoque", salida)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("m"):
        indice = (indice + 1) % len(filtros)
    elif key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
