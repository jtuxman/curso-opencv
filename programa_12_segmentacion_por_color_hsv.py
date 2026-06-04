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

# En OpenCV, una imagen BGR mezcla color y brillo en sus tres canales.
# HSV separa mejor la informacion:
#   H = Hue / Matiz       -> el color principal (0 a 179 en OpenCV)
#   S = Saturation        -> que tan puro o intenso es el color (0 a 255)
#   V = Value / Brillo    -> que tan claro u oscuro es el pixel (0 a 255)
# Esa separacion hace que HSV sea mas util que BGR para detectar objetos por color.

# Cada color tiene uno o mas rangos HSV. La mayoria usa un solo rango.
# El rojo usa dos porque el matiz rojo esta en los extremos de la escala:
# cerca de 0 y cerca de 179. Este es un detalle importante de HSV en OpenCV.
#
# Cada rango tiene esta forma:
#   ((H_min, S_min, V_min), (H_max, S_max, V_max))
#
# El primer tuple es el limite inferior y el segundo tuple es el limite superior.
# Un pixel queda seleccionado solo si sus tres canales HSV caen dentro del rango.
colores = {
    "Rojo": [
        # Rojo bajo: tonos cercanos a H=0.
        ((0, 80, 80), (10, 255, 255)),

        # Rojo alto: tonos cercanos al final de la escala H=179.
        # Ambos rangos representan rojo y se combinan con bitwise_or.
        ((170, 80, 80), (179, 255, 255)),
    ],
    "Verde": [
        # Verde suele estar aproximadamente entre H=35 y H=85.
        # S_min y V_min evitan detectar grises/oscuros como si fueran verde.
        ((35, 60, 60), (85, 255, 255)),
    ],
    "Azul": [
        # Azul suele ubicarse entre H=90 y H=130.
        ((90, 60, 60), (130, 255, 255)),
    ],
    "Amarillo": [
        # Amarillo ocupa una banda relativamente estrecha de matiz.
        ((20, 60, 60), (35, 255, 255)),
    ],
    "Naranja": [
        # Naranja queda entre rojo y amarillo.
        ((10, 80, 80), (25, 255, 255)),
    ],
}

# Lista ordenada para poder ciclar con la tecla 'c'.
# Los diccionarios modernos conservan el orden de insercion, asi que
# list(colores.keys()) produce: Rojo, Verde, Azul, Amarillo, Naranja.
nombres_colores = list(colores.keys())
indice_color = 0

# Vistas disponibles para entender el proceso completo.
# Original  -> frame de camara sin procesamiento.
# Matiz     -> visualizacion del canal H.
# Mascara   -> imagen binaria: blanco=detectado, negro=fondo.
# Resultado -> frame original filtrado por la mascara.
modos = ["Original", "Matiz", "Mascara", "Resultado"]
indice_modo = 0

print("Presiona 'c' para cambiar color objetivo")
print("Presiona 'm' para cambiar vista")
print("Presiona 'q' para salir")

while True:
    ret, frame = cap.read()

    if not ret:
        break

    color_objetivo = nombres_colores[indice_color]
    modo = modos[indice_modo]

    # Convertimos de BGR a HSV para separar matiz, saturacion y brillo.
    # La mascara se calcula en HSV, no en BGR.
    # Si se usaran los rangos HSV sobre frame BGR, los resultados no tendrian
    # sentido porque las posiciones de los canales significarian otra cosa.
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Construimos una mascara acumulando todos los rangos del color elegido.
    # Para rojo habra dos mascaras que se combinan; para los demas colores
    # normalmente solo hay una.
    #
    # Empezamos con None porque no sabemos si el color tendra 1 o 2 rangos.
    # La primera mascara se asigna directamente; las siguientes se combinan.
    mascara = None

    for bajo, alto in colores[color_objetivo]:
        # inRange marca en blanco los pixeles dentro del rango:
        #   bajo[0] <= H <= alto[0]
        #   bajo[1] <= S <= alto[1]
        #   bajo[2] <= V <= alto[2]
        # Todo pixel fuera del rango queda negro.
        mascara_rango = cv2.inRange(hsv, bajo, alto)

        if mascara is None:
            # Primer rango del color: esta sera la base de la mascara.
            mascara = mascara_rango
        else:
            # Si el color tiene mas de un rango, los combinamos con OR.
            # Un pixel queda seleccionado si pertenece a cualquiera de ellos.
            mascara = cv2.bitwise_or(mascara, mascara_rango)

    # Aplicamos la mascara sobre el frame original. Las zonas detectadas
    # conservan su color real; el resto queda negro.
    # Esto facilita verificar visualmente si el color seleccionado realmente
    # corresponde al objeto que queremos detectar.
    resultado = cv2.bitwise_and(frame, frame, mask=mascara)

    # Para visualizar el matiz, fijamos saturacion y brillo al maximo.
    # Asi cada pixel se muestra como su color puro segun el canal H.
    # Esta vista no es la imagen real: es una herramienta didactica para
    # observar como OpenCV interpreta el matiz de cada pixel.
    hsv_matiz = hsv.copy()
    hsv_matiz[:, :, 1] = 255
    hsv_matiz[:, :, 2] = 255
    visual_matiz = cv2.cvtColor(hsv_matiz, cv2.COLOR_HSV2BGR)

    # countNonZero cuenta los pixeles blancos de la mascara.
    # Es una medicion simple de "cuanta imagen" esta siendo detectada.
    # Si el porcentaje es muy alto, probablemente el rango es demasiado amplio.
    # Si es 0, el rango no esta detectando nada en la escena actual.
    pixeles_detectados = cv2.countNonZero(mascara)
    total_pixeles = mascara.shape[0] * mascara.shape[1]
    porcentaje = (pixeles_detectados / total_pixeles) * 100

    if modo == "Original":
        salida = frame
    elif modo == "Matiz":
        salida = visual_matiz
    elif modo == "Mascara":
        # imshow acepta imagenes de 1 canal, pero convertimos a BGR para
        # mantener consistente el formato de salida antes de dibujar texto.
        salida = cv2.cvtColor(mascara, cv2.COLOR_GRAY2BGR)
    else:
        salida = resultado

    etiqueta = (
        f"Vista: {modo}  Color: {color_objetivo}  "
        f"Pixeles: {pixeles_detectados} ({porcentaje:.1f}%)"
    )

    cv2.putText(salida, etiqueta, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv2.putText(salida, "M=vista  C=color  Q=salir", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 2)

    cv2.imshow("Segmentacion por color HSV", salida)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("m"):
        # Cambia entre Original, Matiz, Mascara y Resultado.
        # El modulo hace que al pasar del ultimo modo volvamos al primero.
        indice_modo = (indice_modo + 1) % len(modos)

    elif key == ord("c"):
        # Cambia el color objetivo usando los rangos definidos arriba.
        # Esto permite comparar rapidamente que rangos funcionan mejor
        # con los objetos disponibles frente a la camara.
        indice_color = (indice_color + 1) % len(nombres_colores)

    elif key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
