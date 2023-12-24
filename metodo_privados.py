class inalcanzable():
    __atributo_privado = "Soy un atributo privado"
   
    def __metodo_privado(self):
        print("Soy un método privado")

    def atributo_publico(self):
        print(self.__atributo_privado)

    def metodo_publico(self):
        self.__metodo_privado()
    

inc = inalcanzable()
inc.atributo_publico()
inc.metodo_publico()