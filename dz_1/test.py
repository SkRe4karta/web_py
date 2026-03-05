import subprocess
import pytest
import os

# Для Linux/MAC
INTERPRETER = 'python3'

def run_script(filename, input_data=None):
    """Запускает Python-скрипт и возвращает вывод"""
    # Полный путь к файлу
    filepath = os.path.join('dz_1', filename)
    proc = subprocess.run(
        [INTERPRETER, filepath],
        input='\n'.join(input_data if input_data else []),
        capture_output=True,
        text=True,
        check=False
    )
    return proc.stdout.strip()

def test_hello():
    """Тест hello.py - всегда проходит"""
    result = run_script('hello.py')
    assert result == 'Hello, World!'

@pytest.mark.parametrize("n, expected", [
    ("3", "Weird"),
    ("4", "Not Weird"),
    ("6", "Weird"),
    ("22", "Not Weird"),
    ("1", "Weird"),
    ("20", "Weird"),
    ("2", "Not Weird"),
    ("24", "Not Weird"),
])
def test_python_if_else(n, expected):
    result = run_script('python_if_else.py', [n])
    assert result == expected

@pytest.mark.parametrize("a, b, expected", [
    ("1", "2", ["3", "-1", "2"]),
    ("10", "5", ["15", "5", "50"]),
    ("0", "5", ["5", "-5", "0"]),
    ("-3", "7", ["4", "-10", "-21"]),
    ("100", "100", ["200", "0", "10000"]),
])
def test_arithmetic_operators(a, b, expected):
    result = run_script('arithmetic_operators.py', [a, b]).split('\n')
    assert result == expected

@pytest.mark.parametrize("n, expected", [
    ("1", ["0"]),
    ("3", ["0", "1", "4"]),
    ("5", ["0", "1", "4", "9", "16"]),
    ("7", ["0", "1", "4", "9", "16", "25", "36"]),
    ("10", ["0", "1", "4", "9", "16", "25", "36", "49", "64", "81"]),
])
def test_loops(n, expected):
    result = run_script('loops.py', [n]).split('\n')
    assert result == expected

@pytest.mark.parametrize("n, expected", [
    ("1", "1"),
    ("3", "123"),
    ("5", "12345"),
    ("8", "12345678"),
    ("10", "12345678910"),
])
def test_print_function(n, expected):
    result = run_script('print_function.py', [n])
    assert result == expected

@pytest.mark.parametrize("input_data, expected", [
    (["5", "2", "3", "6", "6", "5"], "5"),
    (["4", "10", "20", "30", "40"], "30"),
    (["5", "-10", "-5", "0", "5", "10"], "5"),
    (["2", "1", "2"], "1"),
])
def test_second_score(input_data, expected):
    result = run_script('second_score.py', input_data)
    assert result == expected

@pytest.mark.parametrize("input_data, expected", [
    (["4", "John", "70", "Jane", "80", "Bob", "80", "Alice", "90"],
     ["Bob", "Jane"]),
    (["2", "First", "100", "Second", "50"],
     ["Second"]),
])
def test_nested_list(input_data, expected):
    result = run_script('nested_list.py', input_data).split('\n')
    assert sorted(result) == sorted(expected)

@pytest.mark.parametrize("input_str, expected", [
    ("Www.MosPolytech.ru", "wWW.mOSpOLYTECH.RU"),
    ("Pythonist 2", "pYTHONIST 2"),
    ("Hello World!", "hELLO wORLD!"),
    ("12345", "12345"),
    ("AaBbCc", "aAbBcC"),
])
def test_swap_case(input_str, expected):
    result = run_script('swap_case.py', [input_str])
    assert result == expected

@pytest.mark.parametrize("input_str, expected", [
    ("this is a string", "this-is-a-string"),
    ("hello world", "hello-world"),
    ("one", "one"),
    ("a b c d", "a-b-c-d"),
    ("Python is awesome", "Python-is-awesome"),
])
def test_split_and_join(input_str, expected):
    result = run_script('split_and_join.py', [input_str])
    assert result == expected

@pytest.mark.parametrize("input_data, expected", [
    (["listen", "silent"], "Yes"),
    (["hello", "world"], "No"),
    (["abc", "abcd"], "No"),
    (["123", "321"], "Yes"),
])
def test_anagram(input_data, expected):
    result = run_script('anagram.py', input_data)
    assert result == expected

@pytest.mark.parametrize("input_data, expected", [
    (["3", "10 20", "15 25", "30 40", "18"], "2"),
    (["2", "5 10", "15 20", "5"], "1"),
    (["2", "5 10", "15 20", "10"], "1"),
    (["2", "5 10", "15 20", "12"], "0"),
    (["1", "0 100", "50"], "1"),
])
def test_metro(input_data, expected):
    result = run_script('metro.py', input_data)
    assert result == expected

@pytest.mark.parametrize("input_str, expected", [
    ("BANANA", "stuart 12"),
    ("AEIOU", "kevin 15"),
    ("BCDFG", "stuart 15"),
    ("A", "kevin 1"),
    ("B", "stuart 1"),
])
def test_minion_game(input_str, expected):
    result = run_script('minion_game.py', [input_str]).lower()
    assert result == expected

@pytest.mark.parametrize("year, expected", [
    ("2000", "True"),
    ("1900", "False"),
    ("2024", "True"),
    ("2023", "False"),
    ("2100", "False"),
])
def test_is_leap(year, expected):
    result = run_script('is_leap.py', [year])
    assert result == expected

@pytest.mark.parametrize("input_data, expected", [
    (["3 2", "1 5 3", "3 1", "5 7"], "1"),
    (["4 2", "1 2 3 4", "1 2", "5 6"], "2"),
    (["4 2", "1 2 3 4", "5 6", "1 2"], "-2"),
    (["4 2", "1 2 3 4", "5 6", "7 8"], "0"),
    (["5 2", "1 1 2 2 3", "1 2", "4 5"], "4"),
])
def test_happiness(input_data, expected):
    result = run_script('happiness.py', input_data)
    assert result == expected

@pytest.mark.parametrize("input_data, expected_items", [
    (["10 3", "золото 5 100", "серебро 4 60", "бронза 3 30"],
     ["золото", "серебро", "бронза"]),
    (["3 2", "платина 5 500", "золото 2 100"],
     ["платина"]),
    (["20 2", "алмаз 5 500", "золото 10 200"],
     ["алмаз", "золото"]),
])
def test_pirate_ship(input_data, expected_items):
    result = run_script('pirate_ship.py', input_data)
    for item in expected_items:
        assert item in result

@pytest.mark.parametrize("input_data, expected", [
    (["1", "5", "7"], ["[35]"]),
])
def test_matrix_mult(input_data, expected):
    result = run_script('matrix_mult.py', input_data).split('\n')
    result = [r.strip() for r in result if r.strip()]
    assert result == expected

def test_max_word():
    """Проверяет, что max_word.py запускается без ошибок"""
    result = run_script('max_word.py', [])
    assert result is not None

def test_price_sum():
    """Проверяет, что price_sum.py запускается без ошибок"""
    result = run_script('price_sum.py', [])
    assert result is not None

lists_cases = [
    (["4", "append 1", "append 2", "insert 1 3", "print"], ["[1, 3, 2]"]),
    (["3", "append 1", "append 2", "print"], ["[1, 2]"]),
    (["7", "append 3", "append 1", "append 2", "sort", "print", "pop", "print"], ["[1, 2, 3]", "[1, 2]"]),
    (["6", "append 1", "append 2", "append 3", "reverse", "print"], ["[3, 2, 1]"]),
]

@pytest.mark.parametrize("input_data, expected_lines", lists_cases)
def test_lists(input_data, expected_lines):
    out = run_script("lists.py", input_data).splitlines()
    assert out == expected_lines

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
