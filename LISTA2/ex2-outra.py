dividendo = int(input("dividendo="))
divisor = int(input("divisor="))
count = 0
if dividendo < 0 or divisor<0:
	exit()
while dividendo >= divisor:
	dividendo = dividendo - divisor
	count = count + 1
print (count)
