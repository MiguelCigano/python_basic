
#Raliza una funcion que se llame recortar

# primer argumento: numeor a evaluar (recortar)
# segundo argumento: limite inferior
# tercer argumento: limite superior

# Acciones a realizar por la funcion
# * devolver el "limite" inferior si el "numero" es menor que este
# * devolver el "limite" superior si el "numero" es mayor que este
# * Si no se supera nigun "limite", devolver el "numero" multiplicado por dos

def recortar(numero, minimo, maximo):
    if numero < minimo:
        print("caso 1")
        return minimo
    elif numero > maximo:
        print("caso 2")
        return maximo
    else:
        print("caso 3")
        return numero

evaluacion = recortar(24, 7, 19)
print(evaluacion)
