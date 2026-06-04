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

# La umbralizacion convierte una imagen en una mascara binaria:
#   255 = blanco  -> pixel seleccionado / objeto / primer plano
#   0   = negro   -> pixel descartado / fondo
# Es uno de los pasos mas importantes antes de encontrar contornos.

# Modos disponibles para comparar diferentes estrategias.
# Original y Gris no son umbralizaciones; se incluyen para comparar
# visualmente contra los resultados binarios.
modos = [
    "Original",
    "Gris",
    "Binaria",
    "Binaria invertida",
    "Adaptativa media",
    "Adaptativa gaussiana",
    "Otsu",
]

# Indice del modo activo. Empieza en 0 = imagen original.
indice = 0

# Umbral manual para los modos "Binaria" y "Binaria invertida".
# En imagenes de 8 bits los pixeles van de 0 a 255:
#   valores <= umbral se consideran oscuros
#   valores >  umbral se consideran claros
umbral = 127

# Valor que tendran los pixeles que cumplan la condicion del umbral.
# 255 significa blanco puro en una imagen de 8 bits.
valor_maximo = 255

# Parametros de la umbralizacion adaptativa:
# block_size define el tamanio de la vecindad local. Debe ser impar y > 1.
# constante_c se resta del promedio local para ajustar la sensibilidad.
block_size = 11
constante_c = 2

print("Presiona 'm' para cambiar modo")
print("Presiona '+' o '-' para ajustar el umbral manual")
print("Presiona 'q' para salir")

while True:
    ret, frame = cap.read()

    if not ret:
        break

    modo = modos[indice]

    # La mayoria de tecnicas de umbralizacion trabajan sobre intensidad,
    # no sobre color. Por eso convertimos BGR (3 canales) a gris (1 canal).
    gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if modo == "Original":
        salida = frame
        etiqueta = "Modo: Original"

    elif modo == "Gris":
        # Convertimos gris a BGR solo para poder escribir texto en color
        # sobre la salida sin depender de una imagen de 1 canal.
        salida = cv2.cvtColor(gris, cv2.COLOR_GRAY2BGR)
        etiqueta = "Modo: Gris"

    elif modo == "Binaria":
        # threshold compara cada pixel contra el umbral:
        #   si pixel > umbral -> 255
        #   si pixel <= umbral -> 0
        # Retorna dos valores:
        #   ret     -> el umbral usado (util con Otsu)
        #   mascara -> imagen binaria resultante
        ret_umbral, mascara = cv2.threshold(
            gris, umbral, valor_maximo, cv2.THRESH_BINARY
        )
        salida = cv2.cvtColor(mascara, cv2.COLOR_GRAY2BGR)
        etiqueta = f"Modo: Binaria  umbral={int(ret_umbral)}"

    elif modo == "Binaria invertida":
        # THRESH_BINARY_INV invierte la regla:
        #   si pixel > umbral -> 0
        #   si pixel <= umbral -> 255
        # Es util cuando el objeto es oscuro y el fondo es claro.
        ret_umbral, mascara = cv2.threshold(
            gris, umbral, valor_maximo, cv2.THRESH_BINARY_INV
        )
        salida = cv2.cvtColor(mascara, cv2.COLOR_GRAY2BGR)
        etiqueta = f"Modo: Binaria invertida  umbral={int(ret_umbral)}"

    elif modo == "Adaptativa media":
        # adaptiveThreshold calcula un umbral diferente para cada zona
        # de la imagen usando el promedio de una vecindad local.
        # Funciona mejor que un umbral global cuando la iluminacion
        # no es uniforme en todo el frame.
        mascara = cv2.adaptiveThreshold(
            gris,
            valor_maximo,
            cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY,
            block_size,
            constante_c,
        )
        salida = cv2.cvtColor(mascara, cv2.COLOR_GRAY2BGR)
        etiqueta = f"Modo: Adaptativa media  block={block_size}  C={constante_c}"

    elif modo == "Adaptativa gaussiana":
        # En lugar de promedio simple, este modo usa promedio ponderado:
        # los pixeles cercanos al centro tienen mas peso que los lejanos.
        mascara = cv2.adaptiveThreshold(
            gris,
            valor_maximo,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            block_size,
            constante_c,
        )
        salida = cv2.cvtColor(mascara, cv2.COLOR_GRAY2BGR)
        etiqueta = f"Modo: Adaptativa gaussiana  block={block_size}  C={constante_c}"

    else:
        # Otsu calcula automaticamente el mejor umbral global para separar
        # dos grupos de pixeles: fondo y objeto. Antes suavizamos un poco
        # para reducir ruido y estabilizar el valor calculado.
        gris_suave = cv2.GaussianBlur(gris, (5, 5), 0)
        umbral_otsu, mascara = cv2.threshold(
            gris_suave, 0, valor_maximo, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )
        salida = cv2.cvtColor(mascara, cv2.COLOR_GRAY2BGR)
        etiqueta = f"Modo: Otsu  umbral_calculado={int(umbral_otsu)}"

    cv2.putText(salida, etiqueta, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)
    cv2.putText(salida, "M=cambiar  +/-=umbral manual  Q=salir", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 2)

    cv2.imshow("Umbralizacion", salida)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("m"):
        # Ciclamos entre todos los modos disponibles.
        indice = (indice + 1) % len(modos)

    elif key == ord("+"):
        # Subimos el umbral sin pasar de 255.
        # Un umbral mas alto exige pixeles mas claros para volverse blancos.
        umbral = min(255, umbral + 5)

    elif key == ord("-"):
        # Bajamos el umbral sin pasar de 0.
        # Un umbral mas bajo hace que mas pixeles se vuelvan blancos.
        umbral = max(0, umbral - 5)

    elif key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
