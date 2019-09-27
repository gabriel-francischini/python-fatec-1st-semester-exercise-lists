#Questão 8 Lista 2

Numero = int(input("Digite o numero:"))
NumSeguinte = Numero
Algarismo = 0
Contador = ""

while NumSeguinte != 0:
    
    Algarismo = NumSeguinte % 2
    NumSeguinte = NumSeguinte // 2
    Contador = str(Algarismo) + Contador

print (Contador)
