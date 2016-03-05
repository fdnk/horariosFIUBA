#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Analisis estadístico de la densidad de cursos en cada día de la semana"""
import sys
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

import parser_horarios

parser_horarios.debug = True

class Grilla:
    def __init__(self, hora_inicio=7, hora_fin=23, fracciones_hora=2):
        """Las horas son [inicio, fin)"""
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.fracciones_hora = fracciones_hora
        self.cantidad_dias_semana = 6
        
        self.grilla = np.zeros( (int((self.hora_fin-self.hora_inicio)*self.fracciones_hora), self.cantidad_dias_semana), dtype=int )

    def __discretizar_hora(self, hora):
        if hora > self.hora_fin:
            raise ValueError("Hora debe ser menor que "+self.hora_fin)
        return int((hora-self.hora_inicio)*self.fracciones_hora)
    
    def cargar_curso(self, curso):
        for h in curso.horario:
            self.cargar_horario(h)
    
    def cargar_horario(self, horario):
        dia=horario[0]
        inicio=horario[1]
        fin=horario[2]
        # Resto uno en día porque arranca en 1 (Arreglar)
        self.grilla[self.__discretizar_hora(inicio):self.__discretizar_hora(fin), dia-1] += 1

    def __str__(self):
        return "De ["+str(self.hora_inicio)+", " +str(self.hora_fin) + ")hs\nL M X J V S\n" + str(self.grilla)
        
    def graficar(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        raise NotImplementedError('No entiendo mp')
        
    
def crear_grilla_ocupacion(cursos):
    grilla = Grilla(fracciones_hora=1)
    i=0
    for curso in cursos:
        # Selecciono los del depto de electrónica plan '86
        if int(curso.codigo/100)==66:
            i=i+1
            grilla.cargar_curso(curso)
    
    print("Cantidad de cursos: %d"%i, file=sys.stderr)    
    
    return grilla

######### main() #########
if __name__ == "__main__":
    # Cargo datos
    archivo_datos = 'Horarios_1Q2016.csv'
    f = open(archivo_datos, 'rb')
    str_data = f.read().decode('utf8', 'ignore') # Esto no me gusta
    f.close()
    
    cursos = parser_horarios.procesar_data(str_data)
    
    grilla = crear_grilla_ocupacion(cursos)
    
    print(grilla)