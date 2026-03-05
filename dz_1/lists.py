arr = []
n = int(input())

commad = ['insert', 'print', 'remove', 'append', 'sort', 'pop', 'reverse']

for i in range(1,n + 1):
    r_comm = input().split()
    if r_comm[0] == commad[0]: arr.insert(int(r_comm[1]),int(r_comm[2]))
    if r_comm[0] == commad[1]: print(arr)
    if r_comm[0] == commad[2]: arr.remove(int(r_comm[1]))
    if r_comm[0] == commad[3]: arr.append(int(r_comm[1]))
    if r_comm[0] == commad[4]: arr.sort()
    if r_comm[0] == commad[5]: arr.pop()
    if r_comm[0] == commad[6]: arr.reverse()
