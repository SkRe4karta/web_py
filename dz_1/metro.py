n = int(input())

pass_time = [list(map(int,input().split())) for i in range(n)]

time = int(input())
count = 0

for i in pass_time:
    if i[0] <= time <= i[1]:
        count += 1
print(count)