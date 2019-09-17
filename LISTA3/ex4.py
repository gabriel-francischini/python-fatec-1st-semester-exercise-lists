#Exercício 04 da lista 3
string = (input("Insira uma sequência de caracteres terminada por ponto(.)"))
char = ""
contador = 0
nova_string = ""
espacos_vistos = 0

#Estruturando a lógica
for character in string: #Para cada caractere na string
    # Acabamos de ver o último espaço em uma sequência de espaços
    if character != " " and char == " ": 
        if espacos_vistos > 1:
            nova_string = nova_string + " "

    if character != " ": # Não é espaço, ignore o caractere
        nova_string = nova_string + character
        espacos_vistos = 0

    # É espaço, fique atento para ver se estamos em uma sequencia de espaços
    if character == " ":
        espacos_vistos = espacos_vistos + 1

    char = character
    contador = contador + 1

if char == ".": #Indica o final da string dada pelo usuário
    print(contador) #Mostra o número de caracteres
    print(nova_string)
