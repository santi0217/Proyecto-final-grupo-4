#  Fecha: 30 de noviembre del 2020
#
#  Autor: Santiago Márquez Álvarez, Sergio Mora Pradilla
#
#  Descripción: El código consiste en la realización de una clase la cual contiene los métodos necesarios para realizar
#  la identificación de placas en una imagen. Estos métodos realizan un procesado de la imagen por diferentes filtros,
#  le analiza sus contornos, le halla su aproximación a un polígono, le halla su relación de aspecto de área, le realiza
#  su correcta homografía, le reconoce los caracteres que están dentro de la placa, guarda esta placa en texto y por
#  ultimo la muestra. Cada uno de estos procesos mencionados anteriormente son procesos separados para su correcto
#  entendimiento.

# Importa las librerias para el procesamiento de imagenes y la deteccion de caracteres
import cv2
import numpy as np
import imutils
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

#Declaracion de la clase
class ReconocimientoPlacas:

    # Inicializacion de algunas variables globales necesarias para los metodos
    def __init__(self):
        self.placas = []
        self.metodo = 0
        self.Finish = False

    # Metodo prepara la imagen para su anaisis
    def pre_procesamiento(self, image):
        img = cv2.imread(image) # Se lee la imagen
        self.image_draw = img.copy()
        self.img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Se convierte a escala de grises
        N = 7 # Ventana de filtrado gaussiano

        #alternativas de filtrado
        if self.metodo == 0: # Filtrado con filtro gaussiano y threshholdin
            image_gauss_lp = cv2.GaussianBlur(self.img_gray, (N, N), 1.5, 1.5)
            ret2, self.bordes = cv2.threshold(image_gauss_lp, 100, 150, cv2.THRESH_BINARY)
        else:# Filtrado lilateral y Canny
            img_bil = cv2.bilateralFilter(self.img_gray, 25, 25, 50)
            self.bordes = cv2.Canny(img_bil, 70, 200)

    #Metodo que encuentra contornos de la imagen
    def contornos(self):
        contourss = cv2.findContours(self.bordes, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # Encuentra contornos
        self.contours = imutils.grab_contours(contourss)
        self.contours = sorted(self.contours, key=cv2.contourArea, reverse=True)[:10] #Organiza los ontornos por area

    #Metodo que aproxima el poligono del contorno
    def approx_Rectangular(self,contorno):
        peri = cv2.arcLength(contorno, True)
        self.approx = cv2.approxPolyDP(contorno, 0.018 * peri, True) # Aporxima el poligono
        self.mask = np.zeros(self.img_gray.shape, np.uint8) # Mascara negra del tamaño de la imagen en grises

    #Metodo que calcula la relacion de aspecto de area del contorno
    def rel_aspecto(self, contorno):
        cx, cy, w, h = cv2.boundingRect(contorno) # Extrae las dimensiones del rectangulo aproximado
        self.aspect_Ratio = float(w) / h #Realiza el calculo

    #Metodo que realiza la homografia del contorno rectangular para corregir la perspectiva y la orientacion
    def homografia(self, screenCnt):

        # Vertices del contorno identificado
        points1 = screenCnt

        #4 posibles maneras de transformar la homografia segun la manera en que se ordenan los vertices hallados
        if screenCnt[1][0][0] > screenCnt[0][0][0] and screenCnt[1][0][1] > screenCnt[0][0][1]:
            if screenCnt[0][0][0] < screenCnt[2][0][0]:
                points2 = [(0, 0), (100, 0), (100, 49), (0, 49)]
            else:
                points2 = [(100, 0), (100, 49), (0, 49), (0, 0)]

        elif screenCnt[1][0][0] < screenCnt[0][0][0] and screenCnt[1][0][1] > screenCnt[0][0][1]:
            if screenCnt[0][0][0] < screenCnt[2][0][0]:
                points2 = [(0, 0), (0, 49), (100, 49), (100, 0)]
            else:
                points2 = [(100, 0), (0, 0), (0, 49), (100, 49)]

        N = 4 # Numero de vertices
        pts1 = np.array(points1[:N]) # establecimiento de vertices del contorno original
        pts2 = np.array(points2[:N]) # establecimiento de vertices del contorno de la homografia
        H, _ = cv2.findHomography(pts1, pts2, method=cv2.RANSAC) #Encuentra la matriz de distorcion entre los puntos
        # Elimina la distorision del contorno original de placa
        self.plate_solo = cv2.warpPerspective(self.image_draw, H, (100, 49))

    #Metodo que identifica los caracteres en la imagen de pla placa reconocida
    def OCR(self):
        # Parametros para filtrar los caracteres deseados y la eficiencia del metodo
        custom_config = r' --psm 6 -c tessedit_char_whitelist=1234567890QWERTYUIOPLKJHGFDSAZXCVBNM'
        self.final = pytesseract.image_to_string(self.plate_solo, config=custom_config)

    # Metodo que guarda la placa identificada y establece que si funciono el filtrado actual
    def guardar_placa(self):
        self.Finish = True
        self.placas = np.append(self.placas, self.final[0:6])

    # Metodo que muestra la placa identificada sola y en la imagen original
    def mostrar_placa(self):
        self.plate_solo = cv2.resize(self.plate_solo, (200, 100)) # Se cambia el tamaño de la imagen de la placa
        cv2.imshow('Placa encontrada ', self.plate_solo)# Se muestra la placa
        cv2.waitKey(200)

        # Se dibuja el contorno en la imagen original
        final_image = cv2.drawContours(self.image_draw, [self.approx], -1,(255, 0, 200), 4 )
        font = cv2.FONT_HERSHEY_PLAIN # Se establece la fuente de letra
        # Se escribe la placa en la coordenada 200,200 con un grosor y color de letra
        cv2.putText(self.image_draw, self.final[0:6],  (200,200), font, 9, (255, 0, 200), 9, cv2.LINE_AA)
        final_image = cv2.resize(final_image, (1000,600)) # Se cambia el tamaño de la imagen para verla mejor
        cv2.imshow('Placa serial ',final_image) #Se muestra la imagen con la placa
        cv2.waitKey(800)





