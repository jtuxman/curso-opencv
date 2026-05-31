import cv2
import time

cap = cv2.VideoCapture(0)

ancho = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
alto = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

if fps == 0:
    fps = 30.0

fourcc = cv2.VideoWriter_fourcc(*"XVID")
grabando = False
writer = None

print("Presiona 'r' para iniciar/detener grabacion, 'q' para salir")

while True:
    ret, frame = cap.read()

    if not ret:
        break

    if grabando and writer is not None:
        writer.write(frame)

    estado = "GRABANDO" if grabando else "EN ESPERA"
    color = (0, 0, 255) if grabando else (0, 255, 0)
    cv2.putText(frame, estado, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    cv2.imshow("Grabar MKV", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("r"):
        if not grabando:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"video_{timestamp}.mkv"
            writer = cv2.VideoWriter(nombre_archivo, fourcc, fps, (ancho, alto))
            grabando = True
            print(f"Grabando: {nombre_archivo}")
        else:
            grabando = False
            writer.release()
            writer = None
            print("Grabacion detenida")

    elif key == ord("q"):
        break

if writer is not None:
    writer.release()

cap.release()
cv2.destroyAllWindows()
