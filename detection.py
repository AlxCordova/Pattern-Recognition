#importamos librerias librerias
import cv2
import numpy as np
import keyboard

#Funcion a la cual se le pasa un parametro dentro del trackbar creado
def z(x):
    pass

#abre la camara
cap = cv2.VideoCapture(1)

#Trackbars para cambiar los valores que se aplican a un filtro HSV
cv2.namedWindow("Trackbars")
cv2.createTrackbar("L-H", "Trackbars", 0, 255, z)
cv2.createTrackbar("L-S", "Trackbars", 0, 255, z)
cv2.createTrackbar("L-V", "Trackbars", 0, 180, z)
cv2.createTrackbar("U-H", "Trackbars", 180, 180, z)
cv2.createTrackbar("U-S", "Trackbars", 255, 255, z)
cv2.createTrackbar("U-V", "Trackbars", 243, 255, z)


font = cv2.FONT_HERSHEY_COMPLEX

while True:
    #captura lo que hay en la camara
    _, frame = cap.read() 
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    l_h = cv2.getTrackbarPos("L-H", "Trackbars")
    l_s = cv2.getTrackbarPos("L-S", "Trackbars")
    l_v = cv2.getTrackbarPos("L-V", "Trackbars")
    u_h = cv2.getTrackbarPos("U-H", "Trackbars")
    u_s = cv2.getTrackbarPos("U-S", "Trackbars")
    u_v = cv2.getTrackbarPos("U-V", "Trackbars")

    #Se le aplican los cambios de colores del trackbar y los almacena dentro de un arreglo
    lower_red = np.array([l_h, l_s, l_v])
    upper_red = np.array([u_h, u_s, u_v])

    #aplica los cambios en el el frame de la mascara, que se encarga de invertir los colores
    mask = cv2.inRange(hsv, lower_red, upper_red)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel)

    # deteccion de contornos
    _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
        x = approx.ravel()[0]
        y = approx.ravel()[1]

        if area > 400:
            cv2.drawContours(frame, [approx], 0, (0, 255, 0), 5)
            #si se presiona "t" muestra los triangulos de la imagen
            if keyboard.is_pressed('t'):
                if len(approx) == 3:
                    cv2.putText(frame, "Triangulo", (x, y), font, 1, (0, 0, 255))
            #si se presiona "r" muestra los cuadros/ rectangulos en la imagen
            elif keyboard.is_pressed('r'):
                if len(approx) == 4:
                    cv2.putText(frame, "Rectangulo", (x, y), font, 1, (255, 0, 0))
            #si se presiona "c" muestra los circulos de la imagen
            elif keyboard.is_pressed('c'):
                if 10 < len(approx) < 20:
                    cv2.putText(frame, "Circulo", (x, y), font, 1, (0, 58, 0))

    #abre las pantallas donde se visualiza lo que captura la camara
    #y la mascara que se le esta aplicando
    cv2.imshow("Video", frame)
    cv2.imshow("Mask", mask)

    #espera que la tecla "ESC" sea presionada para 
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()