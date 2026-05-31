import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # frame.shape retorna una tupla (alto, ancho, canales).
    # Usamos [:2] para quedarnos solo con alto y ancho, ignorando canales.
    # ATENCION: el orden es (alto, ancho) en NumPy, pero los puntos de dibujo
    # en OpenCV usan (x, y) = (ancho, alto). Es una fuente comun de confusion.
    alto, ancho = frame.shape[:2]

    # cv2.rectangle dibuja un rectangulo sobre el frame (lo modifica en lugar).
    # Argumentos: (imagen, esquina_sup_izq, esquina_inf_der, color_BGR, grosor)
    # Color (0, 255, 0) = verde en BGR
    # Grosor 2 = borde de 2 pixeles. Grosor -1 = rectangulo relleno
    cv2.rectangle(frame, (10, 10), (200, 60), (0, 255, 0), 2)

    # Calculamos el centro del frame dividiendo sus dimensiones entre 2.
    # Usamos // (division entera) porque los pixeles son numeros enteros,
    # no pueden tener posicion decimal.
    centro = (ancho // 2, alto // 2)

    # cv2.circle dibuja un circulo.
    # Argumentos: (imagen, centro, radio, color_BGR, grosor)
    # Color (255, 0, 0) = azul en BGR
    # Grosor 3 = borde de 3 pixeles. Grosor -1 = circulo relleno
    cv2.circle(frame, centro, 50, (255, 0, 0), 3)

    # cv2.line dibuja una linea recta entre dos puntos.
    # Argumentos: (imagen, punto_inicio, punto_fin, color_BGR, grosor)
    # (0, 0) es la esquina superior izquierda
    # (ancho, alto) es la esquina inferior derecha
    # Color (0, 0, 255) = rojo en BGR
    cv2.line(frame, (0, 0), (ancho, alto), (0, 0, 255), 1)

    # cv2.putText escribe texto sobre la imagen.
    # Argumentos: (imagen, texto, origen, fuente, escala, color, grosor)
    # El origen (10, alto - 10) posiciona el texto 10px arriba del borde inferior.
    # ATENCION: el origen es la esquina INFERIOR izquierda del texto, no la superior.
    # FONT_HERSHEY_SIMPLEX es la fuente sans-serif estandar de OpenCV.
    # Escala 0.6 = 60% del tamanio original de la fuente.
    # Color (255, 255, 255) = blanco en BGR
    cv2.putText(frame, "Presiona Q para salir", (10, alto - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    cv2.imshow("Dibujo en frame", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
