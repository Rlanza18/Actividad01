# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""
#IMPORTACION DE LAS LIBRERIAS A UTILIZAR
import os

import statistics

import math

import numpy

#COMANDO PARA INDICAR AL PROGRAMA QUE DEBEJE DE EJECUTARSE SOBRE LA CARPETA DONDE SE ENCUENTRA

cwd= os.getcwd()

#CREANDO LISTA PARA ALMACENAR LOS ARCHIVOS DE INTERES (.AS)
lista_AS = []

#FUNCION UTILIZADA PARA FILTRAR LOS ARCHIVOS (.AS) DENTRO DE LA CARPETA EN LA QUE SE EJECUTA EL PROGRAMA
def leer():
    lista_archivos = os.listdir(cwd)

    for archivo in lista_archivos:
        if archivo.endswith(".AS"):
            lista_AS.append(archivo)
   
    print("Se encontraron: ",len(lista_AS)," archivos .AS")
    print ("Ésta es la lista de archivos: \n" , lista_AS)
    return lista_AS
leer()


#FUNCION DE PARA EJECUTAR EL DECODIFICADOR DE ARCHIVOS 
#DE "IDIOMA" DE LA ANTENA A CARACTERES ENTENDIBLES
def obs():
    for mediciones in lista_AS:
        os.system("teqc -O.dec 30 +obs " + mediciones.split("_")[0] + ".o "+ mediciones)

    
obs()   


#FUNCION DEDICADA A EXTRAER LA INFORMACION DE INTERES LA MEDIA DE LAS 
#COORDENADAS MEDIDAS DE ESE DÍA (ARCHIVO POR ARCHIVO), 
#METERLAS EN UNA LISTA PARA CADA UNA (X, Y, y Z) Y
#OBTENER UNA MEDIA DE ESAS MEDIAS
def extraccion():
    x_list = []
    y_list = []
    z_list = []
    lista_archivos = os.listdir(cwd)
    for archivo in lista_archivos:
        if archivo.endswith(".o"):
            extraccion = archivo
            with open(extraccion) as f:
                lineas = f.readlines()[9:10]
                for linea in lineas:
                    coord = linea.strip().split(" ")
                    
                    x = float(coord[0])
                    x_list.append(x)
                    
                    y = float(coord[1])
                    y_list.append(y)
                    
                    z = float(coord[3])
                    z_list.append(z)
                    
    x_mean = statistics.mean(x_list)
    y_mean = statistics.mean(y_list)
    z_mean = statistics.mean(z_list)
    
    print (x_mean,y_mean,z_mean)
    return (x_mean,y_mean,z_mean)

extraccion()

(x_mean, y_mean, z_mean) = extraccion()

#FUNCION DEDICADA A CONVERTIR LAS COORDENADAS A COORDENADAS PLANAS, UTILIZANDO
#SUS RESPECTIVOS ELIPSOIDES
def transformadas(x_mean, y_mean, z_mean):
    print ("¿A cuál elipsiode desea convertir las coordenadas?\n", "A) Clarke 1866\n", "B) GRS80\n","C) WGS84\n")
    entrada = input(str("a, b o c: \n"))
    vc = 0
    
    while vc == 0:
        if entrada == "a":
            vc = 1
            a = 6378206.4
            b = 6356583.8
            
        elif entrada == "b":
            vc = 1
            a = 6378137
            b = 6356752.314
        
        elif entrada == "c" :
            vc = 1
            a = 6378137
            b = 6356752.314
        
        else:
            entrada = input("Por favor introduzca una de las letras válidas en minúscula")
    
    e1 = (((a**2)-(b**2))/(a**2))
    
    e2 = ((((a)**2)-((b)**2))/((b)**2))
    
    p = math.sqrt(((x_mean)**2)+((y_mean)**2))
    
    theta = math.atan((z_mean*a)/(p*b))
    
    phi = math.atan((z_mean+(e2*b*(math.sin(theta)**3))/(p-(e1*a*(math.cos(theta))))))
    
    N = ((a)/(math.sqrt(1-((e1**2)*((math.sin(phi))**2)))))
    
    h =(((p)/(math.cos(theta)))-N)
    
    lamb = math.atan(y_mean/x_mean)
    
    lamb_deg = numpy.degrees (lamb)
    
    phi_deg = numpy.degrees (phi)
    
    print("Las coordenadas son: \n", lamb_deg,phi_deg,h)
    return (lamb_deg, phi_deg, h)
    
transformadas(x_mean, y_mean, z_mean)

(lamb_deg, phi_deg, h) = transformadas(x_mean,y_mean,z_mean)

#FUNCION DEDICADA A LA CREACION Y MODIFICACION DE UN ARCHIVO SEPARADO 
#POR COMILLAS DONDE SE COLOCARAN LAS COORDENADAS FINALES
def csv(lamb_deg,phi_deg,h):
    archivo = open("coordenadas.csv","w")
    
    archivo.write("x, y, z\n")
    archivo.write(str(lamb_deg))
    archivo.write(", ")
    archivo.write(str(phi_deg) )
    archivo.write(", ") 
    archivo.write(str(h))
    archivo.close()
csv(lamb_deg,phi_deg,h)