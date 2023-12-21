class Galleta():
    coco = False

    # constructor de clase
    def __init__(self, precio = None, forma = None):
        self.precio = precio
        self.forma = forma
        if precio is not None and forma is not None:
            print("Se ha creado una galleta que cuesta {} pesos y con forma {}.".format(precio, forma))

    def saborizar(self):
        self.coco = True



UnaGalleta = Galleta(45, "circular")
UnaGalleta.saborizar()
print(UnaGalleta.coco)
