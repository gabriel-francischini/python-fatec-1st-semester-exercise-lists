
string = input("Digite um texto:")
nova_string = ""

acabei_de_ver_espaco = False
for caractere in string:
	if caractere == ' ':
		if acabei_de_ver_espaco == False:
			nova_string = nova_string + ' '
		else:
			pass
	elif caractere != ' ':
		nova_string  = nova_string + caractere
	acabei_de_ver_espaco = (caractere == ' ')

print(nova_string)