numero = int(input('digite o numero: '))

# A gente vai usar o contador para andar pelos números naturais
contador = 0
# Vamos fazer a variável quadrado sempre ser o quadrado do contador
quadrado = contador ** 2

# Aqui andamos pelos números naturais em ordem crescente até
# encontrarmos um quadrado que seja maior que o número (e, portanto,
# por termos andado em ordem crescente, o quadrado anterior tem que
# ser o menor quadrado possível mais próximo do número que o usuário digitou).
while quadrado <= numero:
    # Atualiza contador e quadrado
    contador += 1
    quadrado = contador ** 2

# Volte um contador para trás pois o contador atual é maior que
# o número que o usuário digitou
contador -= 1
quadrado = contador ** 2

print(quadrado)