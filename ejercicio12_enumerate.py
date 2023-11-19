#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 09:43:26 2023

@author: jmiguel
"""

iniciales = ["Hola", "Mundo", "Jesus", "Gric", "Pepe"]

def cadenaInicial(cadenas):
    ls = [None]*len(iniciales)
    for indice, valor in enumerate(cadenas):
        for j,v in enumerate(valor):
            if j==0:
                ls[indice] =  v        
    return ls

print(cadenaInicial(iniciales)) 

iniciales2 = ["Hola", "Mexico", "CUT", "SanDiego", "Tijuana"]

# Recorremos mediante un enumerador cada cadena en la lista
for i,cadena in enumerate(iniciales2):
    # Modificamos cada cadena por su letra inicial
    iniciales2[i] = iniciales2[i][0]

print(iniciales2)       
