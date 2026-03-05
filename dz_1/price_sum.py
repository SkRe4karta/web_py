import csv

f = open('products.csv', encoding= 'utf-8')
arr = []
for i in csv.reader(f):
    arr.append(i[1:])

arr = arr[1:]
sm_1 = float()
sm_2 = float()
sm_3 = float()

f_arr = [[float(x) for x in row] for row in arr]

for i in f_arr:
    sm_1 += i[0]
    sm_2 += i[1]
    sm_3 += i[2]

print(round(sm_1, 2), round(sm_2,2), round(sm_3,2))

