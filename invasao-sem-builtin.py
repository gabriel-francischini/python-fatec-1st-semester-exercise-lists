# Esse código tenta resolver a lista de exercícios "INVASÃO" de ALP


def se_par(numero):
    """Retorna se um número é par (boolean)."""
    return numero % 2 == 0


def soma_dos_digitos(soma):
    """Soma os dígitos de um número e retorna esse valor como número."""
    somador = 0

    while int(soma) > 0:
        somador += int(soma) % 10
        soma = int(soma) // 10
    return somador


def soma_da_lista(lista_a_ser_usada):
    """Retorna a soma dos itens de uma lista."""
    if lista_a_ser_usada == []:
        return 0
    else:
        return lista_a_ser_usada[0] + soma_da_lista(lista_a_ser_usada[1:])


def esta_em(elemento, lista):
    """Retorna True se um elemento está na lista, senão retorna False."""
    for i in range(0, len(lista)):
        if lista[i] == elemento:
            return True

    return False


def pedir_numeros_para_o_usuario(entrada):
    """Transforma uma sequência de caracteres (entrada) em uma lista de números.

    Esta docstring segue o modelo da Google:
        https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html
        http://google.github.io/styleguide/pyguide.html

    Qualquer caractere que não seja um dígito é usado como marcador para separar os números.

    Args:
        entrada (str): Uma sequência/lista de caracteres contendo números.
            Se o argumento entrada for "", isso é um sinal para esta função pedir "pessoalmente"
            um input do usuário. Caso o contrário, a própria variável entrada será usada como uma
            string contendo os números inseridos pelos usuários.

    Retorna:
        Uma lista de números.
    """
    lista_de_numeros = []

    numero_atual = 0
    digitos_do_numero_atual = 0

    # Se a entrada for "" é um sinal que nós mesmos temos que pedir a entrada ao usuário.
    # Quando estamos testando essa função, vale a pena dar entradas diferentes de ""
    # para simular entradas que o usuário tivesse colocado manualmente.
    if entrada == "":
        entrada = input("Digite os numeros separados por espaços:")

    for i in range(0, len(entrada)):
        caractere = entrada[i]

        # Se o número for um dígito, continue calculando o número atual
        if esta_em(caractere, '0123456789') != False:
            numero_atual = numero_atual * 10 + int(caractere)
            digitos_do_numero_atual = digitos_do_numero_atual + 1

        # Se um dos caracteres não for um número, quer dizer que chegamos no
        # final do número anterior e temos que ver se devemos adicionar esse número
        # para a nossa lista_de_numeros
        else:
            # Verifica se por acaso não digitamos dois espaços consecutivos
            if digitos_do_numero_atual > 0:
                # Ok, é um número de verdade que o usuário digitou
                lista_de_numeros = lista_de_numeros + [numero_atual]

                # Prepara algumas variáveis para processarmos o próximo número
                numero_atual = 0
                digitos_do_numero_atual = 0

    # Verifica se o último caractere a ser digitado era um número a ser finalizado
    if digitos_do_numero_atual > 0:
        # Ok, é um número de verdade que o usuário digitou
        lista_de_numeros = lista_de_numeros + [numero_atual]

    return lista_de_numeros


# Nessa função criaremos a 2º e 3ºpartes da mensagem
def partes_decodificadas(Codigo):
    # A "Parte formada de M números" inicia na posição 2 (terceiro item) da lista
    ptM_posicao_inicio = 2
    # "Parte formada de M números" terá uma quantidade de elementos igual ao número M da posição 0
    numero_M = Codigo[0]

    # O Ciscato pediu pra limitar M a 5, mas não falou o que fazer caso desse errado
    if numero_M <= 5:
        pass
    else:
        # "None" é um sinal pro programa que algo deu errado e outra input
        # deve ser pedido
        print("ERRO: O número M é maior que 5.")
        return None

    # O final da ptM será igual a posicao de inicio somada ao numeros de elementos
    ptM_posicao_fim = ptM_posicao_inicio + numero_M

    # Aqui transformamos "Parte formada de M números" em  uma lista que representa o intervalo
    # entre a posição 2 e posição final somada a 1, pois o ultimo numero
    # não entra no intervalo
    ptM = Codigo[ptM_posicao_inicio : ptM_posicao_fim]

    # Segundo o Ciscato nenhum dos números M deve ultrapassar (>=) 500

    for i in range(0, len(ptM)):
        if ptM[i] >= 500:
            # Uh-oh, tivemos um erro e precisamos pedir pro usuário redigitar
            print("ERRO: Um dos números M (" + str(ptM[i]) + " é maior que 500.")
            return None

    # A ptN começará na posição seguinte a posição final da ptM
    ptN_posicao_inicio = ptM_posicao_fim

    # A ptN terá uma quantidade de elementos igual ao número da posição 1
    ptN_numero_elementos = Codigo[1]
    if ptN_numero_elementos <= 10:
        pass
    else:
        ptN_numero_elementos = 10
        # "None" é um sinal pro programa que algo deu errado e outra input
        # deve ser pedido
        print("ERRO: O número N é maior que 10.")
        return None


    # O final da ptN será igual a posicao de inicio somada ao numeros de elementos
    ptN_posicao_fim = ptN_posicao_inicio + ptN_numero_elementos

    # Aqui transformamos ptN em  uma lista que representa o intervalo
    # entre a posição de inicio e posição final somada a 1,pois o ultimo numero
    # não entra no intervalo
    ptN = Codigo[ptN_posicao_inicio : ptN_posicao_fim]

    #Aqui a função retorna uma lista composta pelas PtM e ptN
    return [ptM, ptN]


def lista_dos_pares(lista_1, lista_2):
    """Gera uma lista com os elementos da lista_1 e lista_2 "casados".

    A ordem dos pares é garantida a ser similar na mesma ordem que as
    as listas são dadas.

    Args:
        lista_1 (list): Uma lista qualquer.
        lista_2 (list): Outra lista qualquer.

    Retorna:
        Uma lista contendo pares:
            [ (lista_1[0], lista_2[0]),
              (lista_1[1], lista_2[1]),
              (lista_1[2], lista_2[2]),
              ...
            ]
    """
    if len(lista_1) >= len(lista_2):
        ate = len(lista_2)
    else:
        ate = len(lista_1)

    lista_com_pares = []

    for index in range(0, ate):
        lista_com_pares = lista_com_pares + [[lista_1[index], lista_2[index]]]

    return lista_com_pares


def multiplicacao_da_lista(lista_a_ser_usada):
    """Retorna o produto dos itens de uma lista."""
    if lista_a_ser_usada == []:
        return 1
    else:
        return lista_a_ser_usada[0] * multiplicacao_da_lista(lista_a_ser_usada[1:])


def produto_dos_pares(lista_de_pares):
    """Transforma uma lista de pares em uma lista da multiplicação dos pares.

    Ex: [[1, 2], [3, 4], [5, 6]] -> [2, 12, 30]
    Ex: [['a', 1], ['c', 2], ['e', 3]] -> ['a', 'cc', 'eee']

    Args:
        lista_de_pares (lista): Uma lista contendo pares.
    Retorna:
        Uma lista contendo os elementos do resultado da operação "*" aplicada
            a cada par.
    """
    lista_multiplicada = []

    for i in range(0, len(lista_de_pares)):
        lista_multiplicada = lista_multiplicada + [multiplicacao_da_lista(lista_de_pares[i])]

    return lista_multiplicada


def ordenar_lista(lista_original):
    """Cria uma versão ordenada de uma lista.

    Args:
        lista_original (list): Lista a ser ordenada.
    Retorna:
        Uma cópia da lista_original, mas ordenada.
    """
    # Implementação do GnomeSort, copiada da wikipedia
    # veja: https://en.wikipedia.org/wiki/Gnome_sort
    # veja: https://pt.wikipedia.org/wiki/Gnome_sort

    # Faça uma cópia para não modificar a lista original
    lista = list(lista_original)
    pivot = 0
    lista_length = len(lista)
    while pivot < lista_length - 1:
        if lista[pivot] > lista[pivot + 1]:
            temp = lista[pivot + 1]
            lista[pivot + 1] = lista[pivot]
            lista[pivot] = temp
            if pivot > 0:
                pivot -= 2
        pivot += 1
    return lista


def sequencia_A(quantidade):
    """Gera uma lista com `quantidade` termos da sequencia 1, 2, 3, 4, 5..."""
    sequencia = []

    for numero in range(1, quantidade + 1):
        sequencia = sequencia + [numero]

    return sequencia


def metodo_A(lista_N):
    """Dada a lista de números N, calcula o dia e mês seguindo o método A.

    Args:
        lista_N (lista): Lista contendo a terceira parte da mensagem.
    Retorna:
        Uma lista no formato [dia, mes].
    """
    sequencia = sequencia_A(len(lista_N))
    ordenada = ordenar_lista(lista_N)
    print("Lista ordenada: " + str(ordenada))

    pares = lista_dos_pares(ordenada, sequencia)
    print("Multiplicação dos N números ordenados + serie: " + str(pares))

    produtos = produto_dos_pares(pares)
    print("                                             = " + str(produtos))

    numero_S = soma_da_lista(produtos)
    print("Soma dos produtos: " + str(numero_S))

    return [numero_S % 31, numero_S % 12]


def sequencia_B(quantidade):
    """Gera uma lista com `quantidade` termos da sequencia 1, 2, 4, 7, 11..."""
    sequencia = []

    acumulador = 1
    for passo in range(0, quantidade):
        acumulador += passo
        sequencia = sequencia + [acumulador]

    return sequencia


def lista_dos_digitos(numero):
    """Transforma um número em uma lista de seus dígitos."""
    lista = []

    while int(numero) > 0:
        lista = lista + [int(numero) % 10]
        numero = int(numero) // 10

    # Os números serão decompostos em ordem reversa,
    # então temos que inverter o resultado antes de entregá-lo
    # a quem o pediu
    return lista[::-1]


def soma_dos_pares(lista_de_pares):
    """Transforma uma lista de pares em uma lista da soma dos pares.

    Ex: [[1, 2], [3, 4], [5, 6]] -> [3, 7, 11]
    Ex: [['a', 'b'], ['c', 'd'], ['e', 'f']] -> ['ab', 'cd', 'ef']

    Args:
        lista_de_pares (lista): Uma lista contendo pares.
    Retorna:
        Uma lista contendo os elementos do resultado da operação "+" aplicada
            a cada par.
    """
    lista_somada = []

    for i in range(0, len(lista_de_pares)):
        lista_somada = lista_somada + [soma_da_lista(lista_de_pares[i])]

    return lista_somada


def soma_das_sublistas(lista_com_sublistas):
    """Transforma uma lista com sublistas em uma lista da soma das sublistas .

    Ex: [[1, 2], [3, 4, 5], [6, 7, 8, 9]] -> [3, 12, 30]
    Ex: [['a', 'b', 'c'], ['d'], ['e', 'f']] -> ['abc', 'd', 'ef']

    Args:
        lista_com_sublistas (lista): Uma lista contendo sublistas.
    Retorna:
        Uma lista contendo os elementos do resultado da operação "+" aplicada
            a cada lista.
    """
    return soma_dos_pares(lista_com_sublistas)


def dois_ultimos_digitos_de_cada_um(lista_de_numeros):
    lista_dos_ultimos_digitos = []

    for i in range(0, len(lista_de_numeros)):
        digitos = lista_dos_digitos(lista_de_numeros[i])

        if len(digitos) >= 2:
            ultimos_digitos = digitos[-2:]
        else:
            ultimos_digitos = digitos[-1:]

        lista_dos_ultimos_digitos = lista_dos_ultimos_digitos + [ultimos_digitos]

    return lista_dos_ultimos_digitos


def metodo_B(lista_N):
    """Dada a lista de números N, calcula o dia e mês seguindo o método B.

    Args:
        lista_N (lista): Lista contendo a terceira parte da mensagem.
    Retorna:
        Uma lista no formato [dia, mes].
    """
    sequencia = sequencia_B(len(lista_N))
    pares = lista_dos_pares(lista_N, sequencia)
    print("Soma dos N números + serie: " + str(pares))

    somados = soma_dos_pares(pares)
    print("                          = " + str(somados))

    ultimos_digitos = dois_ultimos_digitos_de_cada_um(somados)
    print("Soma dos 2 últimos dígitos: " + str(ultimos_digitos))

    somados = soma_das_sublistas(ultimos_digitos)
    print("                          = " + str(somados))

    numero_S = soma_da_lista(somados)
    print("                          = " + str(numero_S))

    return [numero_S % 31, numero_S % 12]


def corrigir_dia_e_mes(dia, mes):
    maximos_por_mes = [
        31, # Dezembro
        31, # Janeiro
        28, # Fevereiro
        31, # Março
        30, # Abril
        31, # Maio
        30, # Junho
        31, # Julho
        31, # Agosto
        30, # Setembro
        31, # Outubro
        30, # Novembro
    ]

    if dia > maximos_por_mes[mes]:
        # Dia pertence ao próximo mês
        dia = dia - maximos_por_mes[mes]
        mes = mes + 1

        # Verifica se por acaso a data precisa de mais correções
        return corrigir_dia_e_mes(dia, mes)
    elif dia == 0:
        # Dia '0' é para ser interpretado como dia 31 segundo a 1a folha do exercício
        dia = 31

        return corrigir_dia_e_mes(dia, mes)
    elif dia < 0:
        # Dia pertence ao mês anterior
        if mes == 0:
            mes = 11
        else:
            mes = mes - 1

        dia = maximos_por_mes[mes]
        # Verifica se por acaso a data precisa de mais correções
        return corrigir_dia_e_mes(dia, mes)
    else:
        # A data está certa
        return [dia, mes]


def dia_e_mes_para_string(dia, mes):
    nomes_dos_meses = [
        "dezembro",   # 0
        "janeiro",    # 1
        "fevereiro",  # 2
        "março",      # 3
        "abril",      # 4
        "maio",       # 5
        "junho",      # 6
        "julho",      # 7
        "agosto",     # 8
        "setembro",   # 9
        "outubro",    # 10
        "novembro",   # 11
    ]

    return str(dia) + " de " + nomes_dos_meses[mes]

# ⭕⭕  ⭕⭕  ⭕⭕
# --- AQUI COMEÇA O FLUXO PRINCIPAL DO PROGRAMA ---

def resolucao(entrada):
    codigo = pedir_numeros_para_o_usuario(entrada)
    while partes_decodificadas(codigo) == None:
        print("Digite o código novamente pois deu algum erro no que você digitou.")
        codigo = pedir_numeros_para_o_usuario("")

    print("O código é: " + str(codigo))

    segunda_parte = partes_decodificadas(codigo)[0]
    terceira_parte = partes_decodificadas(codigo)[1]

    print("A segunda parte é: " + str(segunda_parte))
    print("A terceira parte é: " + str(terceira_parte))

    soma = soma_da_lista(segunda_parte)
    somador = soma_dos_digitos(soma)

    print("Soma dos M números: " + str(soma))
    print("Soma dos dígitos: " + str(somador))

    if se_par(somador):
        # É par
        print("Usaremos o método A.")
        dia_mes = metodo_A(terceira_parte)
    else:
        # É impar
        print("Usaremos o método B.")
        dia_mes = metodo_B(terceira_parte)

    dia = dia_mes[0]
    mes = dia_mes[1]

    dia_mes_corrigidos = corrigir_dia_e_mes(dia, mes)
    dia = dia_mes_corrigidos[0]
    mes = dia_mes_corrigidos[1]

    data = dia_e_mes_para_string(dia, mes)
    print("Resp.: " + data)

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
