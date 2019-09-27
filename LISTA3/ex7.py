hip2 = lado12 + lado22
lado1 = int(input("Digite um valor para um lado do triangulo retangulo: "))
lado2 = int(input("Digite um valor para um lado do triangulo retangulo: "))

hipotenusa = int(input("Digite um valor para a hipotenusa: "))
if hipotenusa*2 == lado12 + lado2*2 :
    print("Trata-se de um triângulo retângulo")
else:
    print("Não trata-se de um triangulo retângulo")