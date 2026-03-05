def fact_rec(number):
    if number == 0: return 1

    return fact_rec(number-1) * number

def fact_it(number):
    if number == 0: return 1

    final = 1
    for i in range(1,number + 1):
        final *= i

    return final

if __name__ == '__main__':
    import time
    n = int(input())

    start = time.time()
    fact_rec(n)
    end = time.time()
    print(end - start)
        
    start = time.time()
    fact_it(n)
    end = time.time()
    print(end - start)