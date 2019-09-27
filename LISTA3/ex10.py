binario = int(input("Digite um valor para binário: "))
expoente = 0
isolado = 0
soma_isolados = 0
fator_multiplicativo = 0

while binario != 0:
	fator_multiplicativo = binario % 10
	binario = binario // 10
	isolado = fator_multiplicativo*2**expoente
	soma_isolados = isolado + soma_isolados
	expoente = expoente + 1

print(soma_isolados)

