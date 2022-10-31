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


def calc_elem(i_a: int, i_b: int, m_a: MATRIX, m_b: MATRIX, queue: multiprocessing.Queue = None, path: str = None) -> int:
    """Функция вычисление элемента матрицы при перемножении матриц"""
    n = len(m_a[0])  # количество элементов в строке, то есть столбец
    result: int = 0
    for i in range(n):
        result += m_a[i_a][i] * m_b[i][i_b]
    if path:
        queue.put(result)
        write_elem(path, str(result), i_a, i_b, len(m_a), len(m_b[0]))
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
def write_elem(path: str, elem: str, i: int, j: int, len_m_a: int, len_m_b: int) -> None:
    """Функция поэлементной записи вычислений с матрицами в файл"""
    if i == j == 0:
        with open(path, 'w') as file:
            file.write(elem+', ')
    elif j == len_m_b - 1:
        with open(path, 'a+') as file:
            file.write(elem+'\n')
    elif i == len_m_a - 1 and j == len_m_b - 1:
        with open(path, 'a+') as file:
            file.write(elem)
    else:
        with open(path, 'a+') as file:
            file.write(elem+', ')


def pprint(matrix: MATRIX) -> str:
    """Функция для вывода матрицы в консоль"""
    string = ''
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            string += '{:4d} '.format(matrix[i][j])
        string += '\n'
    return string


def random_matrix(n: int) -> MATRIX:
    """Функция создания матрицы случайных чисел по заданной размерности"""
    return [[random.randint(1, 100) for _ in range(n)] for _ in range(n)]


def list_reshaper(matrix_list: list, i: int, j: int) -> MATRIX:
    """Функция преобразования списка чисел в матрицу"""
    matrix_list = reshape(array(matrix_list), (i, j))
    result: MATRIX = [list(elem) for elem in matrix_list]
    return result


def multiply(m_a: MATRIX, m_b: MATRIX, path: str = None) -> Union[MATRIX, str]:
    """Функция переумножающая матрицы"""
    if array(m_a).shape[1] != array(m_b).shape[0]:
        return "Умножение матриц невозможно"
    lines, columns = len(m_a), len(m_b[0])
    if path:
        result: list = []
        queue = multiprocessing.Queue()
        for i in range(lines):
            for j in range(columns):
                process_elem = multiprocessing.Process(target=calc_elem, args=(i, j, m_a, m_b, queue, path))
                process_elem.start()
                result.append(queue.get())
                process_elem.join()
    else:
        args = [(i, j, m_a, m_b) for i in range(lines) for j in range(columns)]
        with multiprocessing.Pool() as pool:
            result: list = pool.starmap(calc_elem, args)
            pool.join()
    return list_reshaper(result, lines, columns)


if __name__ == '__main__':
    a = read_matrix('matrix1.txt')
    b = read_matrix('matrix2.txt')
    result_m = multiply(a, b, 'result_matrix.txt')
    print(pprint(result_m))
