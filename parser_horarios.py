#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Parser de horarios
	Convierte un CSV a una lista de objetos Curso"""

import re
import sys

debug = False

class Curso:
	"""Una clase contenedora para cada curso de las materias"""
	dias_semana_parser = {'lunes':1, 'martes': 2, 'miercoles': 3, 'miércoles': 3, 'jueves': 4, 'viernes':5, 'sabado':6, 'sábado':6}
	dias_semana = {1:'lunes', 2:'martes', 3:'miercoles', 4:'jueves', 5:'viernes', 6:'sabado'}
	
	def __h2dec__(self,data):
		return int(data[0]) + int(data[1])/60
	
	def __init__(self, codigo, str_data):
		self.codigo = int(codigo)
		self.horario = []
		
		#Proceso los datos para obtener los horarios
		horarios=re.findall(r'(lunes|martes|mi.rcoles|jueves|viernes|s.bado)\s(\d+):(\d+)\s(\d+):(\d+)', str_data, flags=re.I)
		
		for x in horarios:
			# Busco el dia en la lista
			dia = self.dias_semana_parser[x[0].lower().lstrip()]
		
			#Ahora convierto a decimal la hora
			inicio = self.__h2dec__(x[1:3])
			fin = self.__h2dec__(x[3:5])
			
			self.horario.append( (dia, inicio, fin) )
		
	def __str__(self):
		return str(self.codigo)+"|"+str(self.horario)

	

def guardar_log(t1, t2):
	"""Dummy, por ahora"""
	if debug:
		print (t1, t2, file=sys.stderr)

def procesar_data(str_data):
	"""Recibe un string con los datos del Guaraní y crea una lista
	con las materias"""

	lista_cursos = [];
	# Hago split entre cada ocurrencia de "materia:"
	# Obtengo algo de la forma
	#	("texto", "codigo", "texto", "codigo",..., "texto")
	lista_parser = re.split(r'(?:materia: )(\d+)', str_data,flags=re.I)

	i=0

	while i< len(lista_parser):
		texto = lista_parser[i]
		try:
			codigo = int(texto)
			# Halle el codigo de la materia, proceso datos
			str_horarios=lista_parser[i+1]
			i=i+2 # Apunto al próximo elemento a procesar
			
			curso_actual = Curso(codigo, str_horarios)
			lista_cursos.append(curso_actual)
			
		except ValueError:
			# Encontre basura
			guardar_log('basura:', texto)
			i=i+1

	return lista_cursos



######### main() #########
if __name__ == "__main__":
	if len(sys.argv) > 1:
		archivo_datos = sys.argv[1]
	else:
		archivo_datos = 'Horarios_1Q2016.csv'
	# Cargo todo el CSV en memoria
	f = open(archivo_datos, 'rb')
		
	str_data = f.read().decode('utf8', 'ignore') # Esto no me gusta
	f.close()

	cursos = procesar_data(str_data)
	
	for curso in cursos:
		print(str(curso))
	
