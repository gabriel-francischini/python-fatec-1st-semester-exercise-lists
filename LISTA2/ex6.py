fator1 = int(input("fator1:"))
fator2 = int(input("fator2:"))
limite = int(input("limite:"))

i = 0
while i < limite:
	if ((i % fator1) == 0) or ((i % fator2) == 0):
		print (i)
	i = i + 1


