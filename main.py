import multiprocessing
from typing import List, Union
from numpy import array, reshape
import random


def file_opener(func):
    """Обработчик исключений при открытии файла"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BaseException as e:
            print("Произошла ошибка при открытии файла:\n", e)
    return wrapper


MATRIX = List[List[int]]


def calc_elem(i_a: int, i_b: int, m_a: MATRIX, m_b: MATRIX, path: str = None) -> int:
    """Функция вычисление элемента матрицы при перемножении матриц"""
    global threadings
    n = len(m_a[0])  # количество элементов в строке, то есть столбец
    result: int = 0
    for i in range(n):
        result += m_a[i_a][i] * m_b[i][i_b]
    if path:
        write_elem(path, str(result), i_a, i_b, m_a)
    return result


@file_opener
def read_matrix(path: str) -> MATRIX:
    """Функция чтения матрицы из файла"""
    with open(path, 'r') as file:
        int_matrix: MATRIX = []
        str_matrix = file.read().split('\n')
        for string in str_matrix:
            gap_matrix = [int(number) for number in string.split(', ')]
            int_matrix.append(gap_matrix)
        return int_matrix


@file_opener
def load_matrix(matrix: MATRIX, path: str) -> None:
    """Функция сохранения матрицы в заданный файл"""
    with open(path, 'w') as file:
        str_matrix = '\n'.join([', '.join([str(i) for i in elem]) for elem in matrix])
        file.write(str_matrix)


@file_opener
def write_elem(path: str, elem: str, i: int, j: int, m_a: MATRIX) -> None:
    """Функция поэлементной записи вычислений с матрицами в файл"""
    if i == j == 0:
        with open(path, 'w') as file:
            file.write(elem+', ')
    elif i == len(m_a) - 1 and j == len(m_a[0]) - 1:
        with open(path, 'a+') as file:
            file.write(elem)
    elif i == len(m_a) - 2:
        with open(path, 'a+') as file:
            file.write(elem+',\n')
    else:
        with open(path, 'a+') as file:
            file.write(elem+', ')


def random_matrix(lines: int, columns: int) -> MATRIX:
    """Функция создания матрицы случайных чисел по заданной размерности"""
    return [[random.randint(1, 100) for _ in range(columns)] for _ in range(lines)]


def list_reshaper(matrix_list: list, i: int, j: int) -> MATRIX:
    """Функция преобразования списка чисел в матрицу"""
    matrix_list = reshape(array(matrix_list), (i, j))
    result: MATRIX = [list(elem) for elem in matrix_list]
    return result


def multiply(m_a: MATRIX, m_b: MATRIX, path: str = None) -> Union[MATRIX, str]:
    """Функция переумножающая матрицы"""
    if array(m_a).shape[0] != array(m_b).shape[1]:
        return "Умножение матриц невозможно"
    lines, columns = len(m_a), len(m_b[0])
    args = [(i, j, a, b) for i in range(lines) for j in range(columns)]
    if path:
        args = [(i, j, a, b, path) for i in range(lines) for j in range(columns)]
    with multiprocessing.Pool() as pool:
        result: list = pool.starmap(calc_elem, args)
    pool.join()
    return list_reshaper(result, lines, columns)


if __name__ == '__main__':
    a = [[1, 2], [3, 4]]
    b = [[4, 5], [6, 7]]
    print(multiply(a, b, 'D:\ССиС и ПпП\pythonProject_multiprocessing\\test.txt'))