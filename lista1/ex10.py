len = 0
ch = 0

while ch != 'Z':
    if (ch == 'a' or ch == 'e' or ch == 'i' or ch == 'o' or ch == 'u'
     or ch == 'A' or ch == 'E' or ch == 'I' or ch == 'O' or ch == 'U'):
        len = len + 1
    ch = input("Digite uma letra: ")

print(len)
