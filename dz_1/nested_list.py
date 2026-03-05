n = int(input())
arr = [[input(),float(input())] for i in range(n)]
arr = sorted(arr)
mx = max(arr, key=lambda x: x[1])[1]
new_arr = [x for x in arr if x[1] != mx]
for i in new_arr:
    if i[1] == max(new_arr, key=lambda x: x[1])[1]:
        print(i[0])
        