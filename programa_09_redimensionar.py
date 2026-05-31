import cv2

cap = cv2.VideoCapture(0)

# Guardamos las dimensiones originales de la camara antes del loop.
# Estas son las dimensiones reales del sensor; las usaremos como base
# para calcular los tamanios escalados en cada iteracion.
ancho_original = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
alto_original = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Lista de factores de escala disponibles.
# 0.25 = 25% del tamanio original (muy pequeno)
# 0.5  = 50%  (mitad)
# 1.0  = 100% (tamanio real de la camara)
# 1.5  = 150% (agrandado)
# 2.0  = 200% (doble)
escalas = [0.25, 0.5, 1.0, 1.5, 2.0]

# Indice inicial: posicion 2 en la lista = escala 1.0 (sin cambio de tamanio)
indice = 2

print("Presiona '+' para agrandar, '-' para reducir, 'q' para salir")

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Obtenemos la escala activa y calculamos las nuevas dimensiones.
    # int() es necesario porque la multiplicacion con float puede producir
    # decimales (ej: 640 * 1.5 = 960.0) y resize requiere enteros.
    escala = escalas[indice]
    nuevo_ancho = int(ancho_original * escala)
    nuevo_alto = int(alto_original * escala)

    # Elegimos el metodo de interpolacion segun si reducimos o agrandamos.
    # La interpolacion define como se calculan los pixeles nuevos o faltantes.
    #
    # INTER_AREA: al reducir, promedia los pixeles que "desaparecen".
    #   Produce imagenes suaves sin el efecto de escalera (aliasing).
    #   Si se usa INTER_AREA para agrandar, la imagen se ve borrosa.
    #
    # INTER_LINEAR: al agrandar, interpola entre pixeles adyacentes.
    #   Buen balance entre velocidad y calidad para escalas > 1.
    #   Si se usa INTER_LINEAR para reducir, pueden aparecer artefactos.
    if escala < 1.0:
        interpolacion = cv2.INTER_AREA
    else:
        interpolacion = cv2.INTER_LINEAR

    # cv2.resize cambia el tamanio del frame.
    # Argumentos: (imagen, (nuevo_ancho, nuevo_alto), interpolation=metodo)
    # ATENCION: el tamanio es (ancho, alto), NO (alto, ancho) como en frame.shape
    # Retorna una nueva imagen; no modifica frame en su lugar.
    frame_redim = cv2.resize(frame, (nuevo_ancho, nuevo_alto), interpolation=interpolacion)

    # Mostramos la escala activa y las dimensiones reales del frame redimensionado
    etiqueta = f"Escala: {escala}x  ({nuevo_ancho}x{nuevo_alto})"
    cv2.putText(frame_redim, etiqueta, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    cv2.imshow("Redimensionar", frame_redim)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("+") and indice < len(escalas) - 1:
        # Avanzamos al siguiente indice solo si no estamos en el ultimo elemento.
        # La condicion indice < len(escalas) - 1 evita salirse del rango de la lista.
        indice += 1
    elif key == ord("-") and indice > 0:
        # Retrocedemos al indice anterior solo si no estamos en el primero.
        # La condicion indice > 0 evita indices negativos.
        indice -= 1
    elif key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
