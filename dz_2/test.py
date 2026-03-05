import pytest
import os
import sys
import math
import random
from pathlib import Path
from unittest.mock import patch

from fact import fact_rec, fact_it
from show_employee import show_employee
from sum_and_sub import sum_and_sub
from process_list import process_list, process_list_gen
from my_sum import my_sum
import my_sum_argv
import files_sort
import file_search
from email_validation import fun
from fibonacci import fibonacci, cube
from average_scores import compute_average_scores
from plane_angle import Point, plane_angle
from phone_number import sort_phone
from people_sort import person_lister, name_format
from complex_numbers import Complex
from circle_square_mk import circle_square_mk


def test_fact_rec_1():
    assert fact_rec(0) == 1

def test_fact_rec_2():
    assert fact_rec(5) == 120

def test_fact_it_1():
    assert fact_it(0) == 1

def test_fact_it_2():
    assert fact_it(5) == 120

def test_show_employee_1():
    assert show_employee("Иванов Иван") == "Иванов Иван: 100000₽"

def test_show_employee_2():
    assert show_employee("Петров Петр", 50000) == "Петров Петр: 50000₽"

def test_show_employee_3():
    assert show_employee("Сидоров Сидор", 0) == "Сидоров Сидор: 0₽"

def test_show_employee_4():
    assert show_employee("Кузнецов Кузьма") == "Кузнецов Кузьма: 100000₽"

def test_show_employee_5():
    assert show_employee("Саша Булкин") == "Саша Булкин: 100000₽"

def test_show_employee_6():
    assert show_employee("Гена Букин") == "Гена Букин: 100000₽"

def test_show_employee_7():
    assert show_employee("Леонель Месси") == "Леонель Месси: 100000₽"

def test_sum_and_sub_1():
    s, sub = sum_and_sub(10, 5)
    assert s == 15 and sub == 5

def test_sum_and_sub_2():
    s, sub = sum_and_sub(-3, -7)
    assert s == -10 and sub == 4

def test_sum_and_sub_3():
    s, sub = sum_and_sub(5.5, 2.2)
    assert abs(s - 7.7) < 1e-10 and abs(sub - 3.3) < 1e-10

def test_sum_and_sub_4():
    s, sub = sum_and_sub(0, 0)
    assert s == 0 and sub == 0


def test_process_list_1():
    assert process_list([1, 2, 3]) == [1, 4, 27]

def test_process_list_2():
    assert process_list([4, 5, 6]) == [16, 125, 36]

def test_process_list_gen_1():
    assert process_list_gen([1, 2, 3]) == [1, 4, 27]

def test_process_list_gen_2():
    assert process_list_gen([4, 5, 6]) == [16, 125, 36]


def test_my_sum_1():
    assert my_sum(1, 2, 3, 4, 5) == 15

def test_my_sum_2():
    assert my_sum(42) == 42

def test_my_sum_3():
    assert my_sum() == 0

def test_my_sum_4():
    assert abs(my_sum(0.1, 0.2, 0.3) - 0.6) < 1e-10

def test_my_sum_5():
    assert my_sum(1, 3, 3, 3, 5) == 15

def test_my_sum_6():
    assert my_sum(1, 4, 4, 4, 5) == 18


def test_my_sum_argv_1():
    with patch.object(sys, 'argv', ['my_sum_argv.py', '1', '2', '3', '4', '5']):
        assert my_sum_argv.my_sum_argv() == 15

def test_my_sum_argv_2():
    with patch.object(sys, 'argv', ['my_sum_argv.py', '42']):
        assert my_sum_argv.my_sum_argv() == 42

def test_my_sum_argv_3():
    with patch.object(sys, 'argv', ['my_sum_argv.py']):
        assert my_sum_argv.my_sum_argv() == 0

def test_my_sum_argv_4():
    with patch.object(sys, 'argv', ['my_sum_argv.py', '1', '2', '3']):
        assert my_sum_argv.my_sum_argv() == 6


def test_files_sort_1(tmp_path):
    d = tmp_path / "test_dir"
    d.mkdir()
    (d / "b.py").write_text("")
    (d / "a.txt").write_text("")
    (d / "c.py").write_text("")
    
    with patch.object(sys, 'argv', ['files_sort.py', str(d)]):
        result = files_sort.files_sort()
        assert result == ['b.py', 'c.py', 'a.txt']

def test_files_sort_2(tmp_path):
    d = tmp_path / "empty_dir"
    d.mkdir()
    
    with patch.object(sys, 'argv', ['files_sort.py', str(d)]):
        result = files_sort.files_sort()
        assert result == []

def test_files_sort_3():
    with patch.object(sys, 'argv', ['files_sort.py', '/nonexistent/path']):
        result = files_sort.files_sort()
        assert result is None

def test_files_sort_4(tmp_path):
    d = tmp_path / "single_dir"
    d.mkdir()
    (d / "file.txt").write_text("")
    
    with patch.object(sys, 'argv', ['files_sort.py', str(d)]):
        result = files_sort.files_sort()
        assert result == ['file.txt']


def test_email_validation_1():
    assert fun("user@example.com") is True

def test_email_validation_2():
    assert fun("user-name@example.ru") is True

def test_email_validation_3():
    assert fun("user@.com") is False

def test_email_validation_4():
    assert fun("@example.com") is False


def test_fibonacci_1():
    assert fibonacci(1) == [0]

def test_fibonacci_2():
    assert fibonacci(2) == [0, 1]

def test_fibonacci_3():
    assert fibonacci(5) == [0, 1, 1, 2, 3]

def test_fibonacci_4():
    assert list(map(cube, fibonacci(5))) == [0, 1, 1, 8, 27]


def test_average_scores_1():
    scores = [(89, 90, 78), (90, 91, 85)]
    result = compute_average_scores(scores)
    assert len(result) == 3

def test_average_scores_2():
    scores = [(85,)]
    result = compute_average_scores(scores)
    assert len(result) == 1

def test_average_scores_3():
    scores = [(100, 100), (100, 100)]
    result = compute_average_scores(scores)
    assert len(result) == 2

def test_average_scores_4():
    scores = [(89, 90, 78, 93, 80), (90, 91, 85, 88, 86), (91, 92, 83, 89, 90.5)]
    result = compute_average_scores(scores)
    assert len(result) == 5


def test_plane_angle_1():
    A = Point(0, 0, 0)
    B = Point(1, 0, 0)
    C = Point(0, 1, 0)
    D = Point(0, 0, 1)
    angle = plane_angle(A, B, C, D)
    assert 45 <= angle <= 90

def test_plane_angle_2():
    A = Point(0, 0, 0)
    B = Point(1, 0, 0)
    C = Point(0, 1, 0)
    D = Point(0, 1, 1)
    angle = plane_angle(A, B, C, D)
    assert 0 <= angle <= 90

def test_plane_angle_3():
    A = Point(1, 0, 0)
    B = Point(0, 1, 0)
    C = Point(0, 0, 1)
    D = Point(1, 1, 0)
    angle = plane_angle(A, B, C, D)
    assert 0 <= angle <= 45

def test_plane_angle_4():
    A = Point(0, 0, 0)
    B = Point(1, 0, 0)
    C = Point(0, 1, 0)
    D = Point(1, 1, 0)
    angle = plane_angle(A, B, C, D)
    assert 180 <= angle <= 270


def test_phone_number_1():
    l = ["07895462130"]
    result = sort_phone(l)
    assert result == ['+7 (789) 546-21-30']

def test_phone_number_2():
    l = ["89875641230"]
    result = sort_phone(l)
    assert result == ['+7 (987) 564-12-30']

def test_phone_number_3():
    l = ["9195969878"]
    result = sort_phone(l)
    assert result == ['+7 (919) 596-98-78']

def test_phone_number_4():
    l = ["07895462130", "9195969878", "89875641230"]
    result = sort_phone(l)
    assert len(result) == 3


def test_complex_1():
    c = Complex(2, 1)
    d = Complex(5, 6)
    result = c + d
    assert abs(result.real - 7.0) < 1e-10 and abs(result.imaginary - 7.0) < 1e-10

def test_complex_2():
    c = Complex(2, 1)
    d = Complex(5, 6)
    result = c - d
    assert abs(result.real - (-3.0)) < 1e-10 and abs(result.imaginary - (-5.0)) < 1e-10

def test_complex_3():
    c = Complex(3, 0)
    mod_result = c.mod()
    assert abs(mod_result.real - 3.0) < 1e-10

def test_complex_4():
    c = Complex(0, 2)
    assert c.real == 0 and abs(c.imaginary - 2) < 1e-10


def test_circle_square_mk_1():
    random.seed(42)
    area = circle_square_mk(1, 100)
    assert isinstance(area, float)
    assert area > 0

def test_circle_square_mk_2():
    random.seed(42)
    area = circle_square_mk(2, 100)
    assert isinstance(area, float)
    assert area > 0

def test_circle_square_mk_3():
    random.seed(42)
    area1 = circle_square_mk(1, 10)
    area2 = circle_square_mk(1, 100)
    assert isinstance(area1, float)
    assert isinstance(area2, float)

def test_circle_square_mk_4():
    random.seed(42)
    area = circle_square_mk(0, 100)
    assert abs(area) < 1e-10