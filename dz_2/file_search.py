import sys
import os

def file_search():
    name = sys.argv[1]
    final = []
    if len(sys.argv) > 1:
       for root, dirs, files in os.walk('.'):
           for file in files:
               if file == name:
                    path = os.path.join(root,file)
                    f = open(path).read().split('\n')
                    try:
                        final = [f[i] for i in range(5)]
                    except: final = f
                    return final
    return f"Файл {name} не найден"                

if __name__ == '__main__':
    print(file_search())
