try:
    import cv2
except ModuleNotFoundError:
    raise SystemExit(
        "No se encontro OpenCV (cv2). Instala las dependencias con:\n"
        "  python -m pip install -r requirements.txt"
    )
import time

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise SystemExit(
        "No se pudo abrir la camara. Verifica que este conectada, "
        "que no la use otro programa y que tengas permisos sobre el dispositivo."
    )

ancho = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
alto = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

if fps == 0:
    fps = 30.0

# XVID es un codec libre de alta calidad compatible con el contenedor MKV.
# MKV (Matroska) es un formato de contenedor abierto sin restricciones de licencia.
# A diferencia de MP4, MKV es mas resistente a corrupcion si el programa
# se cierra abruptamente sin llamar writer.release().
fourcc = cv2.VideoWriter_fourcc(*"XVID")

grabando = False
writer = None

print("Presiona 'r' para iniciar/detener grabacion, 'q' para salir")

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # cv2.flip(frame, 1) voltea la imagen horizontalmente (efecto espejo).
    # flipCode 1 = volteo en eje vertical (izquierda <-> derecha).
    # Se aplica ANTES de writer.write() para que el video grabado
    # tambien quede en espejo, no solo la vista en pantalla.
    frame = cv2.flip(frame, 1)

    # Escribimos el frame ya volteado al archivo de video
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

            # La extension .mkv define el contenedor; el codec XVID define
            # el algoritmo de compresion interno. Son dos cosas distintas.
            nombre_archivo = f"video_{timestamp}.mkv"
            writer = cv2.VideoWriter(nombre_archivo, fourcc, fps, (ancho, alto))

            if writer.isOpened():
                grabando = True
                print(f"Grabando: {nombre_archivo}")
            else:
                writer.release()
                writer = None
                print(f"No se pudo crear el archivo de video: {nombre_archivo}")
        else:
            grabando = False
            writer.release()
            writer = None
            print("Grabacion detenida")

    elif key == ord("q"):
        break

# Cerramos el archivo si el usuario sale mientras esta grabando
if writer is not None:
    writer.release()

cap.release()
cv2.destroyAllWindows()
