a0 =  int(input('digite o primeiro numero: '))

limite = int(input('digite o limite: '))

razao = int(input('digite a razao: '))

contador = 0

for i in range(a0,limite,razao):
    contador += razao
    print(contador)
