# Enunciado:
#   Dada uma série 1, -1/2, 1/3, -1/4, 1/5, ...
#   imprima os 10 primeiros termos, bem como a
#   soma dos mesmos.
#
#
#                 dividendo
#         ,-----,-----,-----,---.
#         .     .     .     .    .
#        / \   / \   / \   / \    .
#        + 1   - 1   + 1   - 1     .
#  soma =  —  +  —  +  —  +  —  + . . .
#          1     2     3     4     .   
#           \   /       \   /     .
#            \ /         \ /     .
#             v           v     .
#              `---------´-----´
#                   divisor
#
#
# Pseudo-código:
#     1. O dividendo é 1, podendo alternar entre +1 e -1.
#     2. No início, o resultado da soma é 0 pois não há
#        nenhum termo até o momento.
#     3. Para cada dividor nos números de 1 a 10:
#         3.1 O termo atual é o resultado da divisão do dividendo pelo divisor.
#         3.2 Imprima o resultado na tela.
#         3.3 Adicione o termo atual ao resultado da soma.
#         3.4 Troque o sinal do dividendo.
#     4. Mostre o resultado na tela.
#

soma = 0
dividendo = 1

# Para cada divisor de 1 a 11, excluindo o 11
for divisor in range(1, 11):
    termo = dividendo / divisor
    print("Termo número " + str(divisor) + ": " + str(termo))
    soma = soma + termo

    # Troca o sinal do dividendo
    dividendo = dividendo * -1

print("Resultado da soma: " + str(soma))
