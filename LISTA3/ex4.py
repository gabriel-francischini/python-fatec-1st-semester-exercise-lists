
string = input("Digite um texto:")
nova_string = str()

sequencia_de_espacos = 0
for caractere in string:
	if caractere == ' ':
		sequencia_de_espacos = sequencia_de_espacos + 1
	elif caractere != ' ':
		if sequencia_de_espacos > 1:
			nova_string = nova_string + ' '
		nova_string  = nova_string + caractere
		sequencia_de_espacos = 0

print(nova_string)
