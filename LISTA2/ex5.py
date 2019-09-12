Limite = int (input("Limite="))
if Limite // 2 == 1:
	Limite = Limite+1

Expoente = 2
Cos = 1
CntDivisor = 2
DevoSomar = False
Número = int(input("Número:"))
NúmerosTermos = 0

while NúmerosTermos <= Limite:

	CntFatorial = 1
	ResFatorial = 1
	LimiteFat = CntDivisor
	while CntFatorial <= LimiteFat:
		ResFatorial = ResFatorial * CntFatorial
		CntFatorial = CntFatorial + 1
		print ("ResFatorial:" + str(ResFatorial))
		print ("CntFatorial:" + str(CntFatorial))
	Divisor = ResFatorial

	if DevoSomar == False:
		Cos = Cos - Número ** Expoente / Divisor
	elif DevoSomar == True:
		Cos = Cos + Número ** Expoente / Divisor

	Expoente = Expoente + 2
	CntDivisor = CntDivisor + 2
	NúmerosTermos = NúmerosTermos + 1

print(Cos)





	

