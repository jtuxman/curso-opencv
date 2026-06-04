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

# Este programa parte de una mascara HSV como la del programa 12.
# La diferencia es que ahora aplicamos operaciones morfologicas para:
#   - eliminar ruido blanco aislado
#   - rellenar huecos negros dentro del objeto
#   - mejorar la mascara antes de buscar contornos
#
# Las operaciones morfologicas NO detectan color por si mismas.
# Primero necesitamos una mascara binaria. Luego la morfologia modifica
# la forma de las zonas blancas de esa mascara.

colores = {
    "Rojo": [
        ((0, 80, 80), (10, 255, 255)),
        ((170, 80, 80), (179, 255, 255)),
    ],
    "Verde": [
        ((35, 60, 60), (85, 255, 255)),
    ],
    "Azul": [
        ((90, 60, 60), (130, 255, 255)),
    ],
    "Amarillo": [
        ((20, 60, 60), (35, 255, 255)),
    ],
    "Naranja": [
        ((10, 80, 80), (25, 255, 255)),
    ],
}

nombres_colores = list(colores.keys())
indice_color = 0

operaciones = [
    "Sin morfologia",
    "Erosion",
    "Dilatacion",
    "Apertura",
    "Cierre",
]
indice_operacion = 0

vistas = [
    "Comparacion",
    "Mascara original",
    "Mascara procesada",
    "Resultado",
]
indice_vista = 0

# Tamanios de kernel disponibles. Todos son impares para tener un pixel central.
tamanios_kernel = [3, 5, 7, 9, 11, 15]
indice_kernel = 1  # empieza en 5x5

# Numero de veces que se aplica la operacion.
iteraciones = 1


def crear_mascara_color(hsv, color_objetivo):
    # Igual que en el programa 12, un color puede tener uno o varios rangos.
    # El caso mas importante es rojo, que usa dos rangos y los une con OR.
    mascara = None

    for bajo, alto in colores[color_objetivo]:
        mascara_rango = cv2.inRange(hsv, bajo, alto)

        if mascara is None:
            # Primer rango: crea la mascara base.
            mascara = mascara_rango
        else:
            # Rangos adicionales: agregan mas pixeles seleccionados.
            mascara = cv2.bitwise_or(mascara, mascara_rango)

    return mascara


def aplicar_morfologia(mascara, operacion, kernel, num_iteraciones):
    # Todas estas operaciones esperan una mascara de 1 canal.
    # En este contexto:
    #   blanco = objeto o region seleccionada
    #   negro  = fondo
    #
    # El parametro iterations repite la misma operacion varias veces.
    # Un kernel grande o muchas iteraciones producen cambios mas agresivos.
    if operacion == "Erosion":
        # Erosion reduce las zonas blancas.
        # Sirve para eliminar puntos blancos pequenos, pero tambien
        # puede adelgazar o desaparecer objetos reales si se exagera.
        return cv2.erode(mascara, kernel, iterations=num_iteraciones)

    if operacion == "Dilatacion":
        # Dilatacion expande las zonas blancas.
        # Sirve para rellenar huecos pequenos, pero tambien puede unir
        # objetos cercanos que deberian quedar separados.
        return cv2.dilate(mascara, kernel, iterations=num_iteraciones)

    if operacion == "Apertura":
        # Apertura = erosion seguida de dilatacion.
        # Elimina ruido blanco aislado y luego recupera parte del tamano
        # del objeto principal.
        # Es comun usarla cuando la mascara tiene puntitos blancos en el fondo.
        return cv2.morphologyEx(
            mascara, cv2.MORPH_OPEN, kernel, iterations=num_iteraciones
        )

    if operacion == "Cierre":
        # Cierre = dilatacion seguida de erosion.
        # Rellena huecos negros pequenos dentro del objeto y luego reduce
        # el crecimiento causado por la dilatacion.
        # Es comun usarla cuando el objeto detectado aparece perforado.
        return cv2.morphologyEx(
            mascara, cv2.MORPH_CLOSE, kernel, iterations=num_iteraciones
        )

    # "Sin morfologia": devolvemos la mascara original para comparar.
    return mascara


print("Presiona 'c' para cambiar color")
print("Presiona 'm' para cambiar operacion morfologica")
print("Presiona 'v' para cambiar vista")
print("Presiona '+' o '-' para cambiar tamanio de kernel")
print("Presiona 'i' para cambiar iteraciones")
print("Presiona 'q' para salir")

while True:
    ret, frame = cap.read()

    if not ret:
        break

    color_objetivo = nombres_colores[indice_color]
    operacion = operaciones[indice_operacion]
    vista = vistas[indice_vista]
    tamanio_kernel = tamanios_kernel[indice_kernel]

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mascara_original = crear_mascara_color(hsv, color_objetivo)

    # getStructuringElement crea el kernel: una pequena matriz que define
    # la vecindad usada para erosionar, dilatar, abrir o cerrar.
    # MORPH_RECT crea un kernel rectangular. Para empezar es el mas facil
    # de interpretar: una vecindad cuadrada de NxN pixeles.
    kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT, (tamanio_kernel, tamanio_kernel)
    )

    mascara_procesada = aplicar_morfologia(
        mascara_original, operacion, kernel, iteraciones
    )

    resultado = cv2.bitwise_and(frame, frame, mask=mascara_procesada)

    if vista == "Comparacion":
        # hconcat pone dos imagenes lado a lado.
        # Esto obliga a que ambas tengan el mismo numero de canales; por eso
        # convertimos las mascaras de gris (1 canal) a BGR (3 canales).
        original_bgr = cv2.cvtColor(mascara_original, cv2.COLOR_GRAY2BGR)
        procesada_bgr = cv2.cvtColor(mascara_procesada, cv2.COLOR_GRAY2BGR)

        cv2.putText(original_bgr, "Original", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(procesada_bgr, "Procesada", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        salida = cv2.hconcat([original_bgr, procesada_bgr])

    elif vista == "Mascara original":
        salida = cv2.cvtColor(mascara_original, cv2.COLOR_GRAY2BGR)

    elif vista == "Mascara procesada":
        salida = cv2.cvtColor(mascara_procesada, cv2.COLOR_GRAY2BGR)

    else:
        # Resultado: muestra la imagen original filtrada con la mascara
        # ya procesada. Si la morfologia mejoro la mascara, aqui se vera
        # un objeto mas completo o con menos ruido alrededor.
        salida = resultado

    # Medimos cuanta mascara blanca habia antes y despues.
    # Esto ayuda a entender el efecto:
    #   erosion/apertura suelen reducir pixeles blancos
    #   dilatacion/cierre suelen aumentar pixeles blancos
    pixeles_originales = cv2.countNonZero(mascara_original)
    pixeles_procesados = cv2.countNonZero(mascara_procesada)
    diferencia = pixeles_procesados - pixeles_originales

    etiqueta = (
        f"Vista: {vista}  Color: {color_objetivo}  Op: {operacion}  "
        f"Kernel: {tamanio_kernel}x{tamanio_kernel}  Iter: {iteraciones}"
    )
    medicion = (
        f"Pixeles original={pixeles_originales}  "
        f"procesada={pixeles_procesados}  dif={diferencia}"
    )

    cv2.putText(salida, etiqueta, (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 2)
    cv2.putText(salida, medicion, (10, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 2)
    cv2.putText(salida, "M=op  V=vista  C=color  +/-=kernel  I=iter  Q=salir",
                (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 2)

    cv2.imshow("Morfologia", salida)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("m"):
        # Cambia entre sin morfologia, erosion, dilatacion, apertura y cierre.
        indice_operacion = (indice_operacion + 1) % len(operaciones)

    elif key == ord("v"):
        # Cambia la vista para inspeccionar el proceso desde diferentes angulos.
        indice_vista = (indice_vista + 1) % len(vistas)

    elif key == ord("c"):
        # Cambia el color de la mascara base.
        indice_color = (indice_color + 1) % len(nombres_colores)

    elif key == ord("+") and indice_kernel < len(tamanios_kernel) - 1:
        # Kernel mas grande: efecto morfologico mas fuerte.
        indice_kernel += 1

    elif key == ord("-") and indice_kernel > 0:
        # Kernel mas pequeno: efecto mas suave.
        indice_kernel -= 1

    elif key == ord("i"):
        # Cicla 1 -> 2 -> 3 -> 1.
        iteraciones = (iteraciones % 3) + 1

    elif key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
