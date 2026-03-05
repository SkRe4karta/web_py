s = input()

gl = 'AEIOUY'
kevin = 0
stuart = 0

n = len(s)

for i in range(n):
    if s[i] in gl:
        kevin += n - i
    else:
        stuart += n - i

if kevin > stuart: print('kevin',kevin)
else: print('stuart', stuart)
