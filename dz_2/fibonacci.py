cube = lambda x: x**3

def fibonacci(n):
    arr = [0, 1]
    if n > 0:
        if n == 1:
            return [0]
        if n == 2:
            return [0, 1] 
        for i in range(2,n):
            arr.append(arr[i-1] + arr[i-2])
        return arr

if __name__ == '__main__':
    n = int(input())
    print(list(map(cube, fibonacci(n))))
