import multiprocessing
from typing import List
from numpy import array, reshape


def file_opener(func):
    """Обработчик исключений при открытии файла"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BaseException as e:
            print("Произошла ошибка при открытии файла:\n", e)
    return wrapper


MATRIX = List[List[int]]


def calc_elem(i_a: int, i_b: int, m_a: MATRIX, m_b: MATRIX, queue: multiprocessing.Queue):
    """Функция вычисление элемента матрицы при перемножении матриц"""
    n = len(m_a[0])
    result = 0
    for i in range(n):
        result += m_a[i_a][i] * m_b[i][i_b]
    queue.put(result)


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
                gap_matrix.append(int(number))
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


def list_reshaper(matrix_list: list, i: int, j: int) -> MATRIX:
    """Функция преобразования списка чисел в матрицу"""
    matrix_list = reshape(array(matrix_list), (i, j))
    result: MATRIX = []
    for elem in matrix_list:
        result.append(list(elem))
    return result


def multiply(m_a: MATRIX, m_b: MATRIX) -> MATRIX:
    """Функция переумножающая матрицы"""
    queue = multiprocessing.Queue()
    result = []
    lines, columns = len(m_a), len(m_b[0])
    for i in range(len(m_a)):
        for j in range(len(m_a[0])):
            process_elem = multiprocessing.Process(target=calc_elem, args=(i, j, m_a, m_b, queue))
            process_elem.start()
            result.append(queue.get())
            process_elem.join()
    return list_reshaper(result, lines, columns)


if __name__ == '__main__':
    a = [[1, 2], [3, 4]]
    b = [[4, 5], [6, 7]]
    print(multiply(a, b))
