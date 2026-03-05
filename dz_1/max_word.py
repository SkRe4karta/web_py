f = open('example.txt', 'r', encoding='utf-8').read()

for i in '!?.,\n;:»«':
    f = f.replace(i, ' ' if i == '\n' else '')


f = f.split(' ')
mx = max(len(i) for i in f)

print([i for i in f if len(i) == mx])
