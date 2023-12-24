""" 
Programación orienta a objetos
Ejercicio óptativo #1

* Crea una clase llamada Punto con sus dos coordenadas X e Y
* Añade un método constructor para crear puntos fácilmente. Sino se recibe una coordenada, su valor será cero.
* Redefine el método __string__ para que al imprimir por pantalla un punto, aparezca en formato (X,Y)
* Añade un método llamado cuadrante que indique a que cuadrante pertenece el punto, o si es el origen.
* Añade un método llamada vector que tome otro punto y calcule el vector resultante entre los dos puntos.

* (Optativo) añade un método llamado distancia que tome el segundo punto y calcule la distancia entre los dos puntos y la muestre por pantalla.

d = sqrt((X1 - X2)^2 + (Y1 -Y2)^2)

"""

import math

class Punto():

    def __init__(self, X=None, Y=None):
        self.X = X
        self.Y = Y
        if X is not None and Y is not None:
            print("El valor de X es {}, y el valor de Y es {}".format(self.X, self.Y))
        else:
            self.X = 0
            self.Y = 0
            print("El valor de X es {}, y el valor de Y es {}".format(self.X, self.Y))

    def __str__(self):
        return "({},{})".format(self.X, self.Y)
    
    def cuadrante(self):
        if self.X <= 0 and self.Y < 0:
            print("Tercer cuadrante")
        elif self.X <0  and self.Y >= 0:
            print("Segundo cuadrante")
        elif self.X > 0 and self.Y <= 0:
            print("Cuarto cuadrante")
        elif self.X > 0 and self.Y >= 0:
            print("Primer cuadrante")
        elif self.X == 0 and self.Y == 0:
            print("Origen")
    
    def vect(self, X2, Y2):
        self.X2 = X2
        self.Y2 = Y2
        print("El segundo punto es: ({}, {})".format(self.X2, self.Y2))
        self.newvecX = self.X + self.X2
        self.newvecY = self.Y + self.Y2
        return print("Resultante es ({}, {})".format(self.newvecX, self.newvecY))



coor = Punto(2, 2)
print(coor)
coor.cuadrante()
coor.vect(4, 2)
