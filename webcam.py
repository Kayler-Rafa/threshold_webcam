import cv2
import numpy as np

# Função obrigatória do trackbar
def nothing(x):
    pass

# Inicializa webcam
cap = cv2.VideoCapture(0)

# Janela do threshold
cv2.namedWindow("Threshold")

# Trackbar
cv2.createTrackbar("Limite", "Threshold", 127, 255, nothing)

while True:

    ret, frame = cap.read()
    if not ret:
        break

    # Converte para cinza
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Valor do limiar
    threshold_value = cv2.getTrackbarPos("Limite", "Threshold")

    # Threshold binário
    _, thresh = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)

    # -------- HISTOGRAMA --------

    hist = cv2.calcHist([gray], [0], None, [256], [0,256])
    hist = hist / hist.max() * 300

    hist_img = np.zeros((300,256,3), dtype=np.uint8)

    for x in range(256):
        cv2.line(
            hist_img,
            (x,300),
            (x,300-int(hist[x][0])),
            (255,255,255),
            1
        )

    # Linha vermelha mostrando o limiar
    cv2.line(
        hist_img,
        (threshold_value,0),
        (threshold_value,300),
        (0,0,255),
        2
    )

    # -------- MOSTRAR JANELAS --------

    cv2.imshow("Imagem Original", frame)
    cv2.imshow("Escala de Cinza", gray)
    cv2.imshow("Threshold", thresh)
    cv2.imshow("Histograma", hist_img)

    # ESC para sair
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()