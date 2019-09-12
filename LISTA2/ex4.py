divsor =  1
somar = True
pi = 0
N = int (input("N="))
if N//2 == 0:
	N = N+1
while divsor <= N:
	if somar == False:
		pi = pi - 4/divsor
	elif somar == True:
		pi = pi + 4/divsor
	divsor = divsor + 2
print(pi)


