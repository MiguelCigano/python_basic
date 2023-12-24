"""
- Las son un tipo compuesto de datos, el más versatil es la lista.
- Normalmente las listas suele contener datos del mismo tipo, pero en Python no tendremos esa limitante.
- Las listas son muy parecidas a las cadenas de caracteres, y permiten el uso de slicing.
"""

numeros = [1, 2, 3, 4, 5]
datos = [24, "Hola", 10, "2023", "Happy_Christmas"]
print(datos[0])
print(numeros[-2:])
print(datos[-1]) # muestra el último elemento de la lista cadena

"""
- Las cadenas de caracteres son inmutables, pero las listas no lo son.
- Podemos concatenar una lista con otra lista
"""

numeros = numeros + [60, 70, 80]
print(numeros)

pares = [0, 2, 4, 5, 8, 10, 12]
print(pares)
pares[3] = 6
print(pares)

"""
- Las lisats en Python cuentan con el método append que en español significa adjuntar, por lo que podemos agregar un elemento al final de la lista
"""

pares.append(14)
print(pares)

"""
- Las listas tambien permiten la asignación por slicing.
- Tambien podemos saber la longuitud de una lista usando el metodo "len()".
"""
abc = ['a', 'b', 'c', 'd', 'f', 'g']
print(abc)
abc[:3] = ['A', 'B' , 'C']
print(abc)
print(len(abc))

"""
- Se pueden crear listas de listas.
"""

numeros = [1, 2, 3]
letras = ['A', 'B', 'C']
cosas = ["Perrito", "Gatito", "Hola_mundo"]

lista_de_lista = [numeros, letras, cosas]
print(lista_de_lista)

"""
- Con un slicing un poco más creativo
"""
print(lista_de_lista[1][0])