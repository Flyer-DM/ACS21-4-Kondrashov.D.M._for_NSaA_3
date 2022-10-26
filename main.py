#import multiprocessing
from typing import List, Union


MATRIX = List[List[Union[int, float]]]


def calc_elem(i_a: int, i_b: int, m_a: MATRIX, m_b: MATRIX) -> Union[int, float]:
    """Функция вычисление элемента матрицы при перемножении матриц"""
    n: int = len(m_a[0])
    result: Union[int, float] = 0
    for i in range(n):
        result += m_a[i_a][i] * m_b[i][i_b]
    return result


def read_matrix(path: str, sep=';') -> MATRIX:
    """Функция чтения матрицы из файла"""
    pass


def load_matrix(path: str, sep=';') -> None:
    """Функция сохранения матрицы в заданный файл"""
    pass


def write_elem(path: str, i: int, j: int, sep=';') -> None:
    """Функция поэлементной записи вычислений с матрицами в файл"""
    pass

