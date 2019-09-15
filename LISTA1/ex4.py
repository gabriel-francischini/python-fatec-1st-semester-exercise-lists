# Dado um número inteiro N e uma lista de N números inteiros,
# imprima a soma dos números da lista.
#
#
# Exemplo de execução:
#     Digite a quantidade de números na lista: 3
#     Digite o número #1 da lista: 1
#     Digite o número #2 da lista: 2
#     Digite o número #3 da lista: 3
#     Soma é 6.
#
#
# Pseudo-codigo:
#     1. O valor "quantidade" (ex: 3) é digitado pelo usuário. Este valor
#        representa a quantidade de números que devemos receber do usuário.
#     2. No início, a soma de todos os números da lista é 0, pois o usuário ainda
#        não digitou nenhum número, apesar que já sabemos (graças ao passo 1)
#        quantos números devemos receber.
#     3. Repita "quantidade" (ex: 3) vezes:
#         3.1 Um número "numero" (ex: 1, 2, 3, etc.) é digitado pelo usuário.
#         3.2 Adicione esse número à soma total.
#     4. Imprima a soma

# Quantidade de números que devemos receber do usuário
quantidade = int(input("Digite a quantidade de números na lista: "))

# Resultado da soma
soma = 0

# Para cada número que o usuário disse que ia digitar, receba um número
for vez in range(0, quantidade):
    # Use "str(vez+1)" pois o "vez" começa a contar a partir do 0, mas seres
    # humanos contam a partir do 1.
    numero = int(input("Digite o número #" + str(vez + 1) + " da lista: "))
    # Nós calculamos a soma pedaço por pedaço, de cada número em cada número...
    soma = soma + numero

print("Soma é " + str(soma) + ".")
