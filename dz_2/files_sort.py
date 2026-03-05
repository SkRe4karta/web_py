import os
import sys

def files_sort():
    path = sys.argv[1]
    res = []
    if os.path.isdir(path):
        items = os.listdir(path)
        files = []
        for i in items:
            f_path = os.path.join(path, i)
            if os.path.isfile(f_path):
                files.append(i)
        set_file ={}
        for file in files:
            pat, text = os.path.splitext(file)
            if text not in set_file:
                set_file[text] = []
            set_file[text].append(file)
        for text in sorted(set_file.keys()):
            for f in sorted(set_file[text]):
                res.append(f)
        return res


if __name__ == '__main__':
    for f in files_sort():
        print(f)


    



