import cv2
import time

cap = cv2.VideoCapture(0)

print("Presiona 's' para guardar una captura, 'q' para salir")

contador = 0

while True:
    ret, frame = cap.read()

    if not ret:
        break

    cv2.imshow("Camara", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("s"):
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"captura_{timestamp}_{contador}.png"
        cv2.imwrite(nombre_archivo, frame)
        print(f"Captura guardada: {nombre_archivo}")
        contador += 1

    elif key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
