class Pelicula:
    # constructor de clase
    def __init__(self, titulo, duracion):
        self.titulo = titulo
        self.duracion = duracion
        print("Se ha creado la pelicula", self.titulo)

    def __del__(self):
        print("se ha borrado la pelicula", self.titulo)


p = Pelicula("Gladiador", 120)
del(p)

