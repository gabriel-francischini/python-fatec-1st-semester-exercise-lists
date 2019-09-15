#  8. Dado um número inteiro positivo N, calcule e imprima o maior
# quadrado menor ou igual a N. Exemplo: N = 38, o maior quadrado que é menor ou
# igual a 38 é 36, imprimir 36.

limite = int(input("Digite o N: "))

menor_numero_satisfatorio = 1

for numero in range(0, limite + 1):
    quadrado = numero * numero

    if quadrado <= limite:
        menor_numero_satisfatorio = numero

print(menor_numero_satisfatorio)
