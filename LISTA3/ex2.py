limite = int(input("Digite o N#: "))
acumulador = 0
for i in range(1, limite):
	acumulador = acumulador + 1/i

print(acumulador)