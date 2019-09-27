sinal_positivo = False

soma = 0
divisor = 2
x = 1
contador = 0
multiplicacao = 1

numero_final = int(input('digite o número da fatorial: '))

for divisor in range(2, numero_final + 1, 2):
    expoente = divisor
    for numero_fatorial in range(2, numero_final + 1):
        multiplicacao *= numero_fatorial
    if sinal_positivo == False:
        soma -= x ** expoente / multiplicacao
        sinal_positivo = True
    else:
        soma += x ** expoente / multiplicacao
        sinal_positivo = False
    print(soma)

print(soma)