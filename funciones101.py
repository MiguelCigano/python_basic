"""
Created on Sun Nov 19 05:07:24 2023

@author: jmiguel
"""

# paso de variable por valor

def doblar_valor(numero):
    numero*=2
    print(numero)
    
numero = 10 
doblar_valor(numero)
print(numero)

# paso de lista por valor usando for con indice

def doblar_lista(lis_n):
    i = 0
    for n in lis_n:
        lis_n[i] *= 2
        i+=1

ls = [10, 20, 30]
doblar_lista(ls)
print(ls)

# paso de lista por valor usando for y función enumerate

def doblar_lista2(lis_n2):
    for i, n in enumerate(lis_n2):
        lis_n2[i] = lis_n2[i]*2

ls2 = [20, 100, 350]
doblar_lista(ls2)
print(ls2)





