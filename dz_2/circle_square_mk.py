import math
import random

def circle_square_mk(r,n):
    s = 0
    for _ in range(n):
        x = random.uniform(0,r)
        y = random.uniform(0,r)
        if x ** 2 + y ** 2 <= r ** 2:
            s += 1
    pi = (s/n) * 4
    return pi * r ** 2


if __name__ == '__main__':
    n = int(input())
    r = float(input())
    pi = circle_square_mk(r,n)

    print(pi)
    print(math.pi * r**2)   