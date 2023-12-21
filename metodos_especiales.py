class Pelicula:
    # constructor de clase
    def __init__(self, titulo, duracion):
        self.titulo = titulo
        self.duracion = duracion
        print("Se ha creado la pelicula", self.titulo)
    
    # destructor de clase
    def __del__(self):
        print("Se ha borrado la pelicula", self.titulo)

    # redefinimos el método string
    def __str__(self):
        return "{} {}".format(self.titulo, self.duracion)

    def __len__(self):
        return self.duracion    


p = Pelicula("Gladiador", 120)
print(str(p))
print(len(p))


