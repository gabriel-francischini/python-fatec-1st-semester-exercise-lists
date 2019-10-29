import functools
import itertools
import operator

import utilidades
import diames


def partes_decodificadas(codigo):
    """Pega o que usuário digitou e divide em 2 listas. """

    # codigo[0] indica o tamanho da parteM e codigo[1] indica o
    # tamanho da parteN. A parteN começa logo após a parteM.
    # A parteM começa na posição 2 (terceiro elemento)
    ptM = codigo[2:2 + codigo[0]]
    ptN = codigo[(2 + codigo[0]):(2 + codigo[0]) + codigo[1]]

    return (ptM, ptN)

def metodo_A(lista_N):
    """Dada a lista de números N, calcula o dia e mês seguindo o método A.

    Args:
        lista_N (lista): Lista contendo a terceira parte da mensagem.
    Retorna:
        Uma lista no formato [dia, mes].
    """
    # CUIDADO, A LISTA ABAIXO É INFINITA!
    sequencia = itertools.count(1)
    ordenada = sorted(lista_N)
    print("Lista ordenada: " + str(ordenada))

    pares = list(zip(ordenada, sequencia))
    print("Multiplicação dos N números ordenados + serie: " + str(pares))

    produtos = list(map(lambda x: functools.reduce(operator.mul, x, 1),
                        pares))
    print("                                             = " + str(produtos))

    numero_S = sum(produtos)
    print("Soma dos produtos: " + str(numero_S))

    return [numero_S % 31, numero_S % 12]

# CUIDADO, ISSO GERA UMA LISTA INFINITA!
def sequencia_B():
    """Gera uma lista INFINITA com a sequencia 1, 2, 4, 7, 11..."""
    acc = 1
    step = 0
    while True:
        acc += step
        step += 1
        yield acc

def metodo_B(lista_N):
    """Dada a lista de números N, calcula o dia e mês seguindo o método B.

    Args:
        lista_N (lista): Lista contendo a terceira parte da mensagem.
    Retorna:
        Uma lista no formato [dia, mes].
    """

    sequencia = sequencia_B()
    pares = list(zip(lista_N, sequencia))
    print("Soma dos N números + serie: " + str(pares))

    somados = list(map(sum, pares))
    print("                          = " + str(somados))


    ultimos_digitos = list(map(utilidades.ultimos_2_digitos, somados))
    print("Soma dos 2 últimos dígitos: " + str(ultimos_digitos))

    somados = list(map(sum, ultimos_digitos))
    print("                          = " + str(somados))

    numero_S = sum(somados)
    print("                          = " + str(numero_S))

    return [numero_S % 31, numero_S % 12]


def resolucao(entrada):
    codigo = utilidades.number_list_from_string(entrada)
    print("O código é: " + str(codigo))

    segunda_parte, terceira_parte = partes_decodificadas(codigo)
    print("A segunda parte é: " + str(segunda_parte))
    print("A terceira parte é: " + str(terceira_parte))

    soma = sum(segunda_parte)
    print("Soma dos M números: " + str(soma))

    soma_dos_digitos = sum(utilidades.digits_from(soma))
    print("Soma dos dígitos: " + str(soma_dos_digitos))

    if (soma_dos_digitos % 2) == 0:
        # É par
        print("Usaremos o método A.")
        dia, mes = metodo_A(terceira_parte)
    else:
        # É impar
        print("Usaremos o método B.")
        dia, mes = metodo_B(terceira_parte)

    data = diames.DiaMes(dia, mes)
    print("Resp.: " + str(data))

    return data



testes = [
    "3 4 50 2 13 67 4 23 18",
    "5, 6, 22, 122, 34, 67, 89, 32, 189, 25, 53, 67, 125.",
    "5, 6, 22, 123, 34, 67, 89, 32, 189, 25, 53, 67, 125.",
]

for entrada in testes:
    print("\n\n")
    resolucao(entrada)
    print("\n\n----------\n\n")
