dividendo = int(input('digite o dividendo: '))
divisor = int(input('digite o divisor: '))
contador = 0

while (divisor * contador) <= dividendo:
    contador += 1

if divisor * contador - dividendo != 0:
    print(contador - 1)
else:
    print(contador)	
