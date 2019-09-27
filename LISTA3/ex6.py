N = int(input("Digite um valor para N (número de elementos da sequência): "))
numeros = 0
sequencia_atual = 1
maior_sequencia = 0
numero_em_sequencia = None

while numeros < N:
    valor = int(input("Digite um número: "))

    if valor == numero_em_sequencia:
        sequencia_atual += 1
    else:
        sequencia_atual = 1
    if sequencia_atual > maior_sequencia:
        maior_sequencia = sequencia_atual
    numero_em_sequencia = valor
    numeros = numeros + 1

print(maior_sequencia)
