n = int(input())
A = {int(input()) for i in range(n)}

A.remove(max(A))
print(max(A))

