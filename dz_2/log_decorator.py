import datetime as date


def function_logger(l_file):
    def decorator(f):
        def wrapper(*args, **kwargs):
            st = date.datetime.now()
            res = f(*args, **kwargs)
            end = date.datetime.now()

            file = open(l_file, 'a', encoding='utf-8')
            file.write(f'{f.__name__}\n')
            file.write(f"{st.strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write(f"{args if args else '-'}\n")
            file.write(f'{kwargs if kwargs else '-'}\n')
            file.write(f'{res if res is not None else '-'}\n')
            file.write(f"{end.strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write(f'{st - end}\n')
            file.close()

            return res
        return wrapper
    return decorator



name = input()

@function_logger(name)
def hello(x):
    return x

result = hello('Word')
print(result)

