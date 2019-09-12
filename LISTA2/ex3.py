expoente = 1
divisor = 50
pexinho = 0
while divisor > 0:
	temporario = 2**expoente/divisor
	pexinho = pexinho + temporario
	expoente = expoente + 1
	divisor = divisor - 1
print(pexinho)
