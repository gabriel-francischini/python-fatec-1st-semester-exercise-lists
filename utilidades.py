def digits_from(numero):
    """Transforma um número em uma lista de seus dígitos."""
    lista = []

    while int(numero) > 0:
        lista = lista + [int(numero) % 10]
        numero = int(numero) // 10

    # Os números serão decompostos em ordem reversa,
    # então temos que inverter o resultado antes de entregá-lo
    # a quem o pediu
    return lista[::-1]

def number_list_from_string(texto):
    """Transforma uma sequência de caracteres (entrada) em uma lista de números.

    Qualquer caractere que não seja um dígito é usado como marcador para separar os números.

    Args:
        entrada (str): Uma sequência/lista de caracteres contendo números.
    Retorna:
        Uma lista de números.
    """

    lista_de_numeros = []
    numero_atual = ''
    for char in texto:
        if char.isdigit():
            numero_atual += char
        else:
            if numero_atual != '':
                lista_de_numeros.append(int(numero_atual))
                numero_atual = ''

    # Adiciona o último número que ficou sobrando do loop anterior
    if numero_atual != '':
        lista_de_numeros.append(int(numero_atual))

    return lista_de_numeros

# Funçãozinha para pegar os últimos dois dígitos de um número
def ultimos_2_digitos(numero):
    digitos = digits_from(numero)
    if len(digitos) >= 2:
        return digitos[-2:]
    else:
        return digitos[-1:]
