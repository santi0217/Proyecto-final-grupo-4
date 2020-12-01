#  Fecha: 30 de noviembre del 2020
#
#  Autor: Santiago Márquez Álvarez, Sergio Mora Pradilla
#
#  Descripción: El código consiste en la utilización de una clase llamada ReconocimientoPlacas
#  la cual permite realizar una función que lee una imagen de entrada, la pre procesa, le haya los contornos,
#  aproxima sus contornos a un rectángulo y según su relación de aspecto de área, se filtra la placa identificada
#  a la cual se le reconoce sus caracteres, para que este resultado se guarde en un arreglo final donde quedan
#  guardadas todas las placas registradas sin duplicarse.

# Importa la clase de ReconocimientoPlacas
from ReconocimentoPlacas import *
import os

#Variables globales del main
num_images = 19
placas_guardadas = []
placas_final = []

#Funcion que realiza el proceso de reconocimeinto de caracteres de la placa identificada en una imagen de entrada
def Reconocer_placa(indice,path):
    RP = ReconocimientoPlacas() # Inicializa la clase
    path_file = os.path.join(path,'PLACA_'+str(indice)+'.jpg') #Analiza el numero de imagen de placa segun el main

    #Si el primer metodo no reconocio la placa, se prueba con el otro metodo
    while RP.Finish is False:
        RP.pre_procesamiento(path_file) #Se prepara la imagen para su analisis
        RP.contornos() #Se extraen los contornos de la imagen

        #Para cada contorno
        for c in RP.contours:
            RP.approx_Rectangular(c) # Se aproxima a un rectangulo
            if len(RP.approx) == 4: # Si este conotrono aproximado tiene 4 coordenadas o vertices
                RP.rel_aspecto(c) #Se realiza su relacion de aspecto de area

                if RP.aspect_Ratio > 0.8 and RP.aspect_Ratio < 1.6: # Si se cumple el rango de la relacion de aspecto
                    RP.homografia(RP.approx) #Se realiza una homografia para mostrar mejor
                    RP.OCR() #Se realiza su reconocimiento de caracteres
                    if len(RP.final) > 5: # Si el contorno reconocio mas de 5 caracteres
                        RP.guardar_placa() # Se guarda la placa
                        break # Se descartan los otros contornos

        if RP.Finish is False: # Si no se reconocio placa
            RP.metodo = 1 #Se cambia de metodo
    RP.mostrar_placa() # Se muestra la placa y su reconocimiento en la imagen original
    print(RP.placas) # Se imprime la placa identificada
    return RP.placas # se retorna esta placa

#Funcion que elimina los duplicados de placas
def filtrar_duplicados(placas,placas_final):
    for plate in placas:
        if plate not in placas_final:# Si la placa en cuestion no esta en el vector final de placas
            placas_final.append(plate) #Se guarada la placa en el vector final
    return placas_final

# funcion principal main
if __name__ == '__main__':
    #se pide la ruta de la carpeta con las imagenes de las placas
    path = input("Escriba la ruta de la carpeta donde se encuentran las imagenes")
    for i in range(num_images): # Para el numero de placas a identificar
       plate = Reconocer_placa(i+1,path) # se reconoce la placa
       placas_guardadas = np.append(placas_guardadas, plate) # se almacena la placa

    placas_final = filtrar_duplicados(placas_guardadas,placas_final) #Se eliminan duplicados
    print(placas_final) #Se muestran las placas guardadas finalmente


