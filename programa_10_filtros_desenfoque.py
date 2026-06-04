try:
    import cv2
except ModuleNotFoundError:
    raise SystemExit(
        "No se encontro OpenCV (cv2). Instala las dependencias con:\n"
        "  python -m pip install -r requirements.txt"
    )

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise SystemExit(
        "No se pudo abrir la camara. Verifica que este conectada, "
        "que no la use otro programa y que tengas permisos sobre el dispositivo."
    )

# Lista de filtros disponibles para ciclar con 'm'
filtros = ["Sin filtro", "Gaussiano", "Mediano", "Bilateral"]

# Indice del filtro activo. Empieza en 0 = sin filtro
indice = 0

print("Presiona 'm' para cambiar filtro, 'q' para salir")

while True:
    ret, frame = cap.read()

    if not ret:
        break

    filtro = filtros[indice]

    if filtro == "Gaussiano":
        # GaussianBlur aplica un desenfoque suavizando con una funcion gaussiana.
        # Cada pixel se reemplaza por el promedio ponderado de sus vecinos,
        # donde los vecinos mas cercanos tienen mayor peso.
        # Argumentos: (imagen, (ancho_kernel, alto_kernel), sigmaX)
        # Kernel (15, 15): area de 15x15 pixeles de influencia. Mayor = mas borroso.
        # El kernel siempre debe tener tamanio IMPAR (3, 5, 7, 9, 11, 13, 15...).
        # sigmaX=0: OpenCV calcula la desviacion estandar automaticamente.
        # Es el filtro mas rapido; ideal para pre-procesado antes de Canny.
        salida = cv2.GaussianBlur(frame, (15, 15), 0)

    elif filtro == "Mediano":
        # medianBlur reemplaza cada pixel por la MEDIANA de su vecindad.
        # A diferencia del promedio gaussiano, la mediana ignora los valores
        # extremos, lo que lo hace ideal para eliminar ruido tipo "sal y pimienta"
        # (pixeles blancos o negros aislados que aparecen en sensores con ruido).
        # Argumento ksize: tamanio del kernel (debe ser impar y mayor que 1).
        # ksize=15: vecindad de 15x15 = 225 pixeles; toma el valor del centro al ordenarlos.
        salida = cv2.medianBlur(frame, 15)

    elif filtro == "Bilateral":
        # bilateralFilter suaviza la imagen pero PRESERVA LOS BORDES.
        # Es mas lento que Gaussiano y Mediano, pero produce mejor resultado visual.
        # Funciona con dos pesos simultaneos:
        #   1. Peso espacial (sigmaSpace): pixeles mas cercanos influyen mas
        #   2. Peso de color (sigmaColor): pixeles con color similar influyen mas;
        #      pixeles muy distintos en color (bordes) NO se mezclan entre si
        # Argumentos: (imagen, d, sigmaColor, sigmaSpace)
        #   d=9:          diametro del vecindario (9 pixeles de radio)
        #   sigmaColor=75: diferencia de color maxima para mezclar (0-255)
        #   sigmaSpace=75: influencia de pixeles segun su distancia espacial
        salida = cv2.bilateralFilter(frame, 9, 75, 75)

    else:
        # Sin filtro: mostramos el frame original sin ninguna modificacion
        salida = frame

    # Mostramos el nombre del filtro activo sobre la imagen
    cv2.putText(salida, f"Filtro: {filtro}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("Filtros de desenfoque", salida)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("m"):
        # Ciclamos entre los filtros usando modulo para volver al inicio
        # cuando llegamos al ultimo: 0->1->2->3->0->1->...
        indice = (indice + 1) % len(filtros)
    elif key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
