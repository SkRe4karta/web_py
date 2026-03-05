def process_list(arr):
    result = []
    for i in arr:
        if i % 2 == 0:
            result.append(i**2)
        else:
            result.append(i**3)
    return result

def process_list_gen(arr):
     return [i**2 if i % 2 == 0 else i**3 for i in arr]

if __name__ == "__main__":
    n = int(input())
    arr = [int(input()) for _ in range(n)]

    print(process_list(arr))
    print(process_list_gen(arr))