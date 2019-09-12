
n = int(input("Coloque o número N: "))
unidades = n % 10
dezenas = n // 10

if unidades == dezenas:
	print("É igual")
else:
	print("Não é igual")