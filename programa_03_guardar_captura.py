import cv2
import time  # modulo de la libreria estandar para trabajar con fechas y horas

cap = cv2.VideoCapture(0)

print("Presiona 's' para guardar una captura, 'q' para salir")

# Contador de capturas en la sesion actual.
# Se usa como parte del nombre de archivo para garantizar unicidad
# si el usuario toma varias fotos en el mismo segundo.
contador = 0

while True:
    ret, frame = cap.read()

    if not ret:
        break

    cv2.imshow("Camara", frame)

    # Guardamos el resultado de waitKey en una variable para poder
    # compararlo con multiples teclas sin llamar waitKey varias veces.
    # Llamar waitKey dos veces en el mismo ciclo causaria retrasos.
    key = cv2.waitKey(1) & 0xFF

    if key == ord("s"):
        # time.strftime genera una cadena de texto con la fecha/hora actual.
        # El formato "%Y%m%d_%H%M%S" produce algo como "20260530_143507":
        #   %Y = año con 4 digitos     (2026)
        #   %m = mes con 2 digitos     (05)
        #   %d = dia con 2 digitos     (30)
        #   %H = hora en formato 24h   (14)
        #   %M = minutos               (35)
        #   %S = segundos              (07)
        # Este formato permite ordenar los archivos cronologicamente por nombre
        timestamp = time.strftime("%Y%m%d_%H%M%S")

        # Construimos el nombre del archivo combinando timestamp y contador.
        # Ejemplo: "captura_20260530_143507_0.png"
        nombre_archivo = f"captura_{timestamp}_{contador}.png"

        # cv2.imwrite guarda el frame actual como imagen en disco.
        # El formato se determina automaticamente por la extension:
        #   .png -> sin perdida de calidad (recomendado para capturas)
        #   .jpg -> con compresion (archivos mas pequenos pero pierde calidad)
        #   .bmp -> sin compresion (archivos grandes)
        cv2.imwrite(nombre_archivo, frame)
        print(f"Captura guardada: {nombre_archivo}")
        contador += 1

    elif key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
