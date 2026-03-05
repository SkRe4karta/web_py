def wrapper(f):
    def fun(l):
        arr = []
        for i in range(len(l)):
            
            cl = l[i][-10:]
            arr.append(f'+7 ({cl[:3]}) {cl[3:6]}-{cl[6:8]}-{cl[8:]}')
        
        return f(arr)
    return fun

@wrapper
def sort_phone(l):
    return sorted(l)

if __name__ == '__main__':
    l = [input() for _ in range(int(input()))]
    print(*sort_phone(l), sep='\n')
