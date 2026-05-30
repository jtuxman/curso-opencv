import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    alto, ancho = frame.shape[:2]

    # Rectangulo en la esquina superior izquierda
    cv2.rectangle(frame, (10, 10), (200, 60), (0, 255, 0), 2)

    # Circulo en el centro del frame
    centro = (ancho // 2, alto // 2)
    cv2.circle(frame, centro, 50, (255, 0, 0), 3)

    # Linea diagonal
    cv2.line(frame, (0, 0), (ancho, alto), (0, 0, 255), 1)

    # Texto en la parte inferior
    cv2.putText(frame, "Presiona Q para salir", (10, alto - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    cv2.imshow("Dibujo en frame", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
