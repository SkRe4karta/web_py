n, m = map(int, input().split())

arr = []
for _ in range(m):
    name, ves, gold = input().split()
    ves = int(ves)
    gold = int(gold)
    arr.append([name, ves, gold])

arr.sort(key= lambda x: x[2] / x[1], reverse=True)

final = []
sum_gr = 0

for i in arr:
    if i[1] <= n-sum_gr:
        sum_gr += i[1]
        final.append(i)

    else: 
        dol = round( (n-sum_gr)/  i[1],2) 
        i[1] = n-sum_gr
        i[2] = i[2] * dol
        final.append(i)
        break

final.sort(key= lambda x: x[2], reverse=True)

for name, ves, gold in final:
    print(f'{name} {ves}  {gold}')