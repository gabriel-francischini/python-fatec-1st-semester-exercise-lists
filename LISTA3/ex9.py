N = int(input("Digite um valor para N: "))
if N <= 0 :
    N = int(input("Digite um valor para N: "))

novo_numero_divisao = N
ultimo_numero = 99

e_crescente = True

while novo_numero_divisao != 0:
    if ultimo_numero > (novo_numero_divisao % 10):
        pass
    else:
        e_crescente = False

    ultimo_numero = novo_numero_divisao % 10
    novo_numero_divisao = novo_numero_divisao // 10

if e_crescente:
    print("É crescente")
else:
    print("Não é crescente")

