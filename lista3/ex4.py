ch = ''
str = ''

spc = 0
while ch != '.':
    if ch != ' ':
        if spc > 1:
            str = str + ' '
        spc = 0
        str = str + ch
    else:
        spc = spc + 1
    ch = input("Digite um character:")

print(str)
