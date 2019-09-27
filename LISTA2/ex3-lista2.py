expoente = 1
divisor = 50

termo = 2**expoente/divisor

soma = 0

for expoente in range(1, 50 + 1):
	termo = 2**expoente/divisor
	soma = soma + termo
	divisor -= 1
	
print(soma)

