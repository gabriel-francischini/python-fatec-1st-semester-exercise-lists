sinal_positivo = True

soma = 0

n = int(input('digite o número de pi: '))

for divisor in range(1, n + 1, 2):
    if sinal_positivo == True:
        soma += 4 / divisor
        sinal_positivo = False
    else:
        soma -= 4 / divisor
        sinal_positivo = True
    print(soma)

print(soma)
