import cv2
import numpy as np


def dibujado(mascara, color, frame, q, color_name):
    # Encuentra contorno 
    contorno,_= cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    detectado = False
    for i in contorno:
        area = cv2.contourArea(i)
        # para detectar objetos cerca de la camara
        if area > 1000:
            nuevo_contorno = cv2.convexHull(i)
            cv2.drawContours(frame, [nuevo_contorno], 0, color,3) 
            if not detectado and q.empty():
                q.put(color_name)
                detectado = True
    if not detectado:
        detectado = False

def captura(q):
    # Formato hsv
    captura = cv2.VideoCapture(0)

    # OpenCv utiliza BGR y se tiene que pasar a HSV con numpy

    rojo_bajo1 = np.array([0, 100, 20], np.uint8)
    rojo_alto1 = np.array([8, 255, 255], np.uint8)

    amarillo_bajo = np.array([25, 185, 20], np.uint8)
    amarillo_alto = np.array([32, 255, 255], np.uint8)

    verde_bajo = np.array([36, 100, 20], np.uint8)
    verde_alto = np.array([63, 255, 185], np.uint8)

    azul_bajo = np.array([100, 65, 75], np.uint8)
    azul_alto = np.array([130, 255, 255], np.uint8)

    rojo_bajo2 = np.array([175, 100, 20], np.uint8)
    rojo_alto2 = np.array([179, 255, 255], np.uint8)

    while True:
        comprobar, frame = captura.read()
        if comprobar == False: break
        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Detecta los colores en la imagen
        maskAmarillo = cv2.inRange(frameHSV, amarillo_bajo, amarillo_alto)
        maskAzul = cv2.inRange(frameHSV, azul_bajo, azul_alto)
        maskRojo1 = cv2.inRange(frameHSV, rojo_bajo1, rojo_alto1)
        maskRojo2 = cv2.inRange(frameHSV, rojo_bajo2, rojo_alto2)
        maskRojo = cv2.add(maskRojo1, maskRojo2)
        maskVerde = cv2.inRange(frameHSV, verde_bajo, verde_alto)

        # Dibuja los contornos de los colores detectados
        dibujado(maskAmarillo, (0, 255, 255), frame, q, "amarillo")
        dibujado(maskAzul, (255, 0, 0), frame, q, "azul")
        dibujado(maskRojo, (0, 0, 255), frame, q, "rojo")
        dibujado(maskVerde, (0, 255, 0), frame, q, "verde")

        cv2.imshow('Detector de colores', frame)
        if cv2.waitKey(1) & 0xFF == ord('0'):
            break

    captura.release()
    cv2.destroyAllWindows()
