#import multiprocessing
from typing import List, Union


def file_opener(func):
    """Обработчик исключений при открытии файла"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BaseException as e:
            print("Произошла ошибка при открытии файла:\n", e)
    return wrapper


MATRIX = List[List[Union[int, float]]]


def calc_elem(i_a: int, i_b: int, m_a: MATRIX, m_b: MATRIX) -> Union[int, float]:
    """Функция вычисление элемента матрицы при перемножении матриц"""
    n: int = len(m_a[0])
    result: Union[int, float] = 0
    for i in range(n):
        result += m_a[i_a][i] * m_b[i][i_b]
    return result


@file_opener
def read_matrix(path: str, sep=';') -> MATRIX:
    """Функция чтения матрицы из файла"""
    with open(path) as file:
        int_matrix: MATRIX = []
        str_matrix = file.read().split(sep+'\n')
        str_matrix[-1] = str_matrix[-1].replace(sep, '')
        for string in str_matrix:
            gap_matrix = []
            for number in string.split(', '):
                gap_matrix.append(float(number) if '.' in number else int(number))
            int_matrix.append(gap_matrix)
        return int_matrix


@file_opener
def load_matrix(matrix: MATRIX, path: str, sep=';') -> None:
    """Функция сохранения матрицы в заданный файл"""
    with open(path, 'w') as file:
        sep = sep + '\n'
        str_matrix = sep.join([', '.join([str(i) for i in elem]) for elem in matrix]) + ';'
        file.write(str_matrix)


def write_elem(path: str, i: int, j: int, sep=';') -> None:
    """Функция поэлементной записи вычислений с матрицами в файл"""
    pass


def multiply(m_a: MATRIX, m_b: MATRIX) -> MATRIX:
    """Функция переумножающая матрицы"""
    pass



# load_matrix([[1, 2.6, 7], [3.3, 4, 8], [5, 6, 10.5]], "D:\ССиС и ПпП\pythonProject_multiprocessing\\test.txt")
# a = read_matrix("D:\ССиС и ПпП\pythonProject_multiprocessing\\test.txt")
# print(a)
