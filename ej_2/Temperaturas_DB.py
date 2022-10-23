# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 11:36:21 2022

@author: alumno
"""

from  Temperaturas_DB import ArbolAVL, NodoArbol 

class Temperaturas_DB:
    
    def __init__(self):
        self.mediciones = ArbolAVL()
        
    def guardar_temperatura(self,temperatura,fecha):
        self.mediciones.agregar(temperatura, fecha)
        
    def devolver_temperatura(self,fecha):
        self.mediciones.obtener(fecha)
        
    # def max_temp_rango(self,fecha1, fecha2):
    #     self.mediciones

    def min_temp_rango(self,fecha1, fecha2):
        self.mediciones 
        
    