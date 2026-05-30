import cv2

cap = cv2.VideoCapture(0)

ancho = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
alto = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
fps = cap.get(cv2.CAP_PROP_FPS)

print(f"Resolución: {int(ancho)} x {int(alto)}")
print(f"FPS: {fps}")

while True:
    ret, frame = cap.read()

    if not ret:
        break

    frame_espejo = cv2.flip(frame, 1)

    cv2.imshow("Camara espejo", frame_espejo)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
