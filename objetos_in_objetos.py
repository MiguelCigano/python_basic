class Alumno():
    
    # constructor de clase de clase Alumno
    def __init__(self, nombre = None, edad = None, grado = None):
        self.nombre = nombre
        self.edad = edad
        self.grado = grado
        print("se ha creado la clase alumno, con: ", self.nombre)
    
    # ...
    def __str__(self):
        return "{} ({})".format(self.nombre, self.edad)


class Lista():
    # se crea una lista vacia como atributo de clase
    lista_inscritos = []

    def __init__(self, lista_inscritos = []):
        self.lista_inscritos = lista_inscritos

    # método interno para agregar alumnos a la lista
    def agregar_alumno(self, alum):
        self.lista_inscritos.append(alum)

    # método interno para mostrar la lista de alumnos
    def mostrar_alumnos(self):
        for alum in self.lista_inscritos:
            print(alum)


# instancia de la clase Alumno        
alum = Alumno("Pedrito Pérez", 29, 3)

# instancia de la clase lista, pasanso "alum" como elemento de una lista
lst = Lista([alum])

# llamado de metodo de clase, para agregar un alumno sin necesidad de instanciar la clase "Alumno"
lst.agregar_alumno(Alumno("María López", 22, 6))

lst.mostrar_alumnos()