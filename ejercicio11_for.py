#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 08:40:51 2023

@author: jmiguel
"""
n = 9 
n2 = 0

def sumatorio(n, n2):
    for i in range(n):
        if i!=5 and i!=7:
            n2 = i + n2
            print(i)
            #print(n2)
    
    n2 = n2 + n
    return n2

n_ = sumatorio(n, n2)
print(sumatorio(n, n2))


# opción 2

# Completa el ejercicio aquí
sumatorio = 0
numero = 9 # esta línea se agrega debido a que no tenemos la libreria evaluate
# Generamos el bucle entre 0 y el numero+1 (para no excluirlo del range)
for n in range(numero+1):
    # Si no es múltiple de 5 y 7 lo sumamos
    if n % 5 != 0 and n % 7 != 0:
        sumatorio += n

print(sumatorio)
