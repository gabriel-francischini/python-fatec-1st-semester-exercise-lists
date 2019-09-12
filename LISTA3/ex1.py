
numero_usuario = int(input("Digite um número: "))

encontrado = False
numero_tentativa = 1
triangular = numero_tentativa * (numero_tentativa + 1) * (numero_tentativa + 2)
while triangular <= numero_usuario:
	if triangular == numero_usuario:
		print("É triangular")
		encontrado = True

	triangular = numero_tentativa * (numero_tentativa + 1 )* (numero_tentativa + 2)
	numero_tentativa = numero_tentativa + 1

if encontrado == False:
	print("Não é triangular")