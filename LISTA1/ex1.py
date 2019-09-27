Matricula = int(input("Digite o numero da Matricula"))

while Matricula != 999:
	Nota1 = float(input("Nota 1:"))

	Nota2 = float(input("Nota 2:"))

	Nota3 = float(input("Nota 3:"))

	media = (2*Nota1 + 3*Nota2 + 4*Nota3)/9

	if media >= 7:
		print("Aprovado")

	else:
		print("Reprovado")

	print(Matricula)

	print(media)