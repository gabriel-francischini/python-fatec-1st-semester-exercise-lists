numero = int(input("Digite um numero: "))

digit_list = []
while numero != 0:
    digit = numero % 10
    numero = numero // 10
    digit_list = [digit] + digit_list

lista_de_digitos = digit_list

last_character = ""
for character in lista_de_digitos:
    if last_character == character:
        print("Os digitos "
              + str(last_character)
              + " e "
              + str(character)
              + " são iguais")

    last_character = character

