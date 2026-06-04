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

# Leemos las dimensiones de la camara ANTES del loop.
# VideoWriter necesita conocer el tamanio exacto de los frames
# al momento de crearse; si los frames enviados tienen otro tamanio
# el video quedara corrupto o en negro.
# int() es necesario porque cap.get() retorna float y VideoWriter requiere int.
ancho = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
alto = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# Algunas camaras o drivers no reportan fps correctamente y devuelven 0.
# Si se pasa fps=0 a VideoWriter el video se crea pero se reproduce
# de forma incorrecta (sin tiempo entre frames). Usamos 30 como valor comun.
if fps == 0:
    fps = 30.0

# VideoWriter_fourcc crea el codigo FourCC del codec de compresion.
# FourCC = Four Character Code: identificador de 4 bytes del algoritmo de video.
# "mp4v" = MPEG-4 Part 2, compatible con contenedores .mp4
# El asterisco * desempaqueta la cadena "mp4v" en 4 caracteres separados:
# equivalente a VideoWriter_fourcc('m','p','4','v')
fourcc = cv2.VideoWriter_fourcc(*"mp4v")

# Estado de la grabacion: False = en espera, True = grabando activamente
grabando = False

# El objeto VideoWriter se crea solo cuando el usuario inicia la grabacion.
# Se inicializa en None para poder verificar si existe antes de llamar write()
writer = None

print("Presiona 'r' para iniciar/detener grabacion, 'q' para salir")

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Si estamos grabando Y el writer existe, escribimos el frame al archivo.
    # La doble condicion evita un error si writer fuera None inesperadamente.
    if grabando and writer is not None:
        writer.write(frame)

    # Indicador visual del estado: rojo cuando graba, verde cuando espera
    estado = "GRABANDO" if grabando else "EN ESPERA"
    color = (0, 0, 255) if grabando else (0, 255, 0)
    cv2.putText(frame, estado, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    cv2.imshow("Grabar video", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("r"):
        if not grabando:
            # Iniciamos una nueva grabacion creando un archivo nuevo.
            # El nombre con timestamp garantiza que cada grabacion sea unica.
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"video_{timestamp}.mp4"

            # cv2.VideoWriter crea el archivo y prepara el codec.
            # Argumentos: (archivo, fourcc, fps, (ancho, alto))
            # ATENCION: el tamanio es (ancho, alto), NO (alto, ancho) como en shape
            writer = cv2.VideoWriter(nombre_archivo, fourcc, fps, (ancho, alto))

            if writer.isOpened():
                grabando = True
                print(f"Grabando: {nombre_archivo}")
            else:
                writer.release()
                writer = None
                print(f"No se pudo crear el archivo de video: {nombre_archivo}")
        else:
            # Detenemos la grabacion.
            # writer.release() finaliza la escritura del archivo y cierra los
            # headers del contenedor MP4. Sin esta llamada el archivo queda
            # incompleto y muchos reproductores no podran abrirlo.
            grabando = False
            writer.release()
            writer = None
            print("Grabacion detenida")

    elif key == ord("q"):
        break

# Salvaguarda: si el usuario sale con 'q' mientras graba, cerramos el archivo
# correctamente para no corromperlo. Es el mismo release() de arriba pero
# aplicado al caso en que el loop termina sin que el usuario detenga la grabacion.
if writer is not None:
    writer.release()

cap.release()
cv2.destroyAllWindows()
