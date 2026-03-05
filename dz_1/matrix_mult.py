n = int(input())

a = [list(map(int, input().split())) for i in range(n)]
b = [list(map(int, input().split())) for i in range(n)]
arr = [[0 for _ in range(n)] for i in range(n)]
for s in range(n):
    for row in range(n):
        for i in range(n):
            arr[s][row] += a[s][i] * b[i][row]
print(*arr)