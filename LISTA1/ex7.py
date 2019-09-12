numero = float(input("Digite o numero:"))
soma = 0
contador = 0
while numero != 99.99:
	print(numero)
	soma = soma + numero
	contador = contador + 1
	numero = float(input("Digite o numero:"))

print(soma/contador)
