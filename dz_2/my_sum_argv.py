import sys

def my_sum_argv():
    args = sys.argv[1:]
    numbers = [int(i) for i in args]
    return sum(numbers)

if __name__ == '__main__':
    print(my_sum_argv())