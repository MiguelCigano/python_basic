variable = 10

def saludar():
    print("Hola, este print se llama desde la funcion saludar()")

saludar()

def tabla_multiplicar():
    for i in range(10):
        print("5 *", i, " = ", i*5)

tabla_multiplicar()

# Nota como esta funcion modifica solo el valor dentro de la funcion
# paso por referencia
def modificar_var(variable):
    variable = variable*2
    print("Variable: ", variable)

modificar_var(variable)
print(variable)

# Esta funcion no necesita que se le pase la variable
def test():
    print(variable)

test()
