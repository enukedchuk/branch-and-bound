import numpy as np
from .exceptions import Incompatible_constraints, Unlimited_function, Iteraions_limit

def simplex_method(matrix,all_variable,dependent_variable):
    """Табличный симплекс-метод
    Параметры:
    matrix - матрица, приведенная к каноническому виду
    all_variable - список всех базисных и свободных перменных по порядку
    dependent_variable - 'f' + список всех базисных переменных по порядку

    На выходе:
    [Словарь {Перменная: значение}, конечная матрица, f + зависимые переменные]"""
    iteratian_sm_limit = 100
    iteration_sm = 0
    while True and iteration_sm<iteratian_sm_limit:
        if np.all(matrix[0, :-1] >= -1e-10):
            result = [dict(zip(dependent_variable, matrix[:, -1])), matrix, dependent_variable]
            r_var = [var for index, var in enumerate(all_variable) if var.startswith('r')]
            if any((r in result[0]) and (result[0].get(r) != 0) for r in r_var):
                raise Incompatible_constraints
            return result

        free = np.divide(matrix[1:, -1],
                         matrix[1:, np.argmin(matrix[0, :-1])],
                         where=(matrix[1:, np.argmin(matrix[0, :-1])] != 0),
                         out=np.full_like(matrix[1:, -1], np.inf))
        free = np.where(free < 0, np.inf, (np.where(np.isclose(free, 0.0) & np.signbit(free), np.inf, free)))
        if all(i == np.inf for i in free):
            raise Unlimited_function
        el_index = np.argmin(free) + 1, np.argmin(matrix[0, :-1])
        dependent_variable[el_index[0]] = all_variable[el_index[1]]
        matrix[el_index[0]] = np.divide(matrix[el_index[0]], matrix[el_index])
        for str in range(len(matrix)):
            for stlb in range(len(matrix[0])):
                if str != el_index[0] and stlb != el_index[1]:
                    matrix[str, stlb] = matrix[str, stlb] - (matrix[el_index[0], stlb] / matrix[el_index]) * matrix[
                        str, el_index[1]]
        matrix[el_index[0]] = np.divide(matrix[el_index[0]], matrix[el_index])
        matrix[:, el_index[1]] = [0] * len(matrix)
        matrix[el_index] = 1
    if iteration_sm>=iteratian_sm_limit:
        raise Iteraions_limit

def dual_simplex(matrix,all_variable,dependent_variable):
    """Двойственный симплекс-метод
    Параметры:
    matrix - матрица, приведенная к каноническому виду
    all_variable - список всех базисных и свободных перменных по порядку
    dependent_variable - 'f' + список всех базисных переменных по порядку

    На выходе:
    [Словарь {Перменная: значение}, конечная матрица, f + зависимые переменные]
    """
    if np.all(matrix[1:, -1] >= -1e-10):
        return [dict(zip(dependent_variable, matrix[:,-1])),matrix, dependent_variable]
    indx = np.argmin(matrix[:,-1])
    free = np.divide(matrix[0,:-1],
                     matrix[indx, :-1],
                     where=(matrix[indx, :-1] != 0),
                     out=np.full_like(matrix[0,:-1], np.inf))*(-1)
    free = np.where(free < 0, np.inf, (np.where(np.isclose(free, 0.0) & np.signbit(free), np.inf, free)))
    if all(i==np.inf for i in free):
        raise Exception
    el_index = indx, np.argmin(free)
    dependent_variable[el_index[0]] = all_variable[el_index[1]]
    matrix[el_index[0]] = np.divide(matrix[el_index[0]], matrix[el_index])
    for str in range(len(matrix)):
        for stlb in range(len(matrix[0])):
            if str != el_index[0] and stlb != el_index[1]:
                matrix[str, stlb] = matrix[str, stlb] - (matrix[el_index[0], stlb] / matrix[el_index]) * matrix[str, el_index[1]]
    matrix[el_index[0]] = np.divide(matrix[el_index[0]], matrix[el_index])
    matrix[:, el_index[1]] = [0] * len(matrix)
    matrix[el_index] = 1
    return(dual_simplex(matrix,all_variable,dependent_variable))


