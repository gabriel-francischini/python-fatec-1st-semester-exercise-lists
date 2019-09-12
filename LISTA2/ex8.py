

numero = int(input("Digite o numero em base decimal: "))

acumulador = ""

while numero != 0:
	algarismo = numero % 2
	numero = numero // 2
	acumulador = str(algarismo) + acumulador 

print(acumulador)
