n, m = map(int, input().split())

arr = list(map(int, input().split()))[:n]

a = list(map(int, input().split()))[:m]
b = list(map(int, input().split()))[:m]

happy = 0

for x in arr:
    if x in a:
        happy += 1
    elif x in b:
        happy -= 1

print(happy)

