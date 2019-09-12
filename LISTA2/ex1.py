matricula = ""

while True:
	matricula = int(input ("matricula:"))
	if matricula == 999:
		break
	nota1 = int(input("Nota 1:"))
	nota2 = int(input("Nota 2:"))
	nota3 = int(input("Nota 3:"))
	média = (2*nota1 + 3*nota2 + 4*nota3)/9
	print(média)
	print (matricula)
	if média >= 7:
		print ("aprovado")
	else:
		print("reprovado")

