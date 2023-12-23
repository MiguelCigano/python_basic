class Alumno():
    
    # constructor de clase
    def __init__(self, nombre = None, edad = None, grado = None):
        self.nombre = nombre
        self.edad = edad
        self.grado = grado
        print("se ha creado la clase alumno, con: ", self.nombre)
    
    def __str__(self):
        return "{} ({})".format(self.nombre, self.edad)


class Lista():
    # se crea una lista vacia como atributo
    lista_inscritos = []

    # se crea el constructor de esta clase
    # se inicializa el atributo de clase con...
    def __init__(self, lista_inscritos = []):
        self.lista_inscritos = lista_inscritos

    # método interno para agregar alumnos a la lista
    def agregar_alumno(self, al):
        self.lista_inscritos.append(al)

    # método interno para mostrar la lista de alumnos
    def mostrar_alumnos(self):
        for al in self.lista_inscritos:
            print(al)

al = Alumno("Pedrito", 29, 3)
lst = Lista([al])
lst.agregar_alumno(Alumno("María López", 22, 6))

lst.mostrar_alumnos()