numero = 0

contador = 0

soma = 0

while numero != 99.99:
    numero = float(input('digite um numero: '))
    if numero != 99.99:
        print(numero)
        soma += numero
        contador += 1
    else:
        pass

print(soma/contador)    