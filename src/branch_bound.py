import numpy as np
from typing import Optional
from src import math_frame as mf
from src import matrix_utils as mu
from tkinter.messagebox import showerror
from anytree import Node, RenderTree
from .exceptions import Incompatible_constraints, Unlimited_function,Iteraions_limit

class Node:
    """Узел дерева

    Параметры:
    matrix - матрица оптимума с данными ограничениями
    all_var - все переменные в решении по порядку
    dependent_var - базисные переменные по порядку
    parent - родительский узел
    children - список ссылок на дочерние узлы
    integer - целочисленность решения (бинарная)"""

    def __init__(self,
                 matrix: np.ndarray,
                 all_var, dependent_var,
                 extr: dict,
                 criteria:  Optional['Node'] = None,
                 parent: Optional['Node'] = None):
        self.matrix = matrix
        self.all_var = all_var
        self.dependent_var = dependent_var
        self.parent = parent
        self.extremum = extr
        self.criteria = criteria
        self.children = []
        self.integer = self.integer_check(self.extremum)

    def integer_check(self, solution): #Проверка целочисленности
        return all(np.isclose(solution[x],round(solution[x])) for x in solution if x.startswith('x'))


class BranchAndBound_method:
    def __init__(self, matrix,all_var,dependend_var):
        self.matrix = matrix
        self.allvar = all_var
        self.dependend = dependend_var
        self.active_branch = []
        self.root = None
        self.error = None
        try:
            self.finish = self.solve()
        except Exception as e:
            self.error = e
            self.finish = None

    def solve(self): #Решение методом ВИГ
        try:
            root = self.create_root()
        except Exception as a:
            raise a
        self.root = root
        self.active_branch.append([root.extremum['f'],root])
        iteratian_limit = 100
        iteration = 0
        while True and iteration<iteratian_limit:
            best_branch = max(self.active_branch, key=lambda x: x[0])[1]
            if best_branch.integer:
                return best_branch
            criteria = self.find_criteria(best_branch.extremum)
            try:
                matrix_with_restr = mu.adding_restrictions(best_branch.matrix,criteria,best_branch.all_var,best_branch.dependent_var)
            except Exception as e:
                print(e)

            try:
                res1 = mf.dual_simplex(np.copy(matrix_with_restr[0]),matrix_with_restr[2],matrix_with_restr[3])
                children1 = Node(res1[1].copy(), matrix_with_restr[2].copy(), res1[2].copy(), res1[0].copy(), f'{criteria[0]}<={criteria[1]//1}', best_branch)
                best_branch.children.append(children1)
                self.active_branch.append([children1.extremum['f'], children1])
            except:
                pass

            try:
                res2 = mf.dual_simplex(matrix_with_restr[1],matrix_with_restr[2],matrix_with_restr[3])
                children2 = Node(res2[1].copy(), matrix_with_restr[2].copy(), res2[2].copy(), res2[0].copy(), f'{criteria[0]}=>{criteria[1]//1+1}', best_branch)
                best_branch.children.append(children2)
                self.active_branch.append([children2.extremum['f'], children2])
            except:
                pass
            self.active_branch.remove([best_branch.extremum['f'], best_branch])
            iteration+=1
        if iteration >= iteratian_limit:
            raise Iteraions_limit
        raise Exception




    def create_root(self): #Создание дочернего узла
        try:
            res = mf.simplex_method(self.matrix, self.allvar,self.dependend) #extr, matrix, dependend_var
        except Incompatible_constraints as ic:
            showerror('Ошибка', 'Система ограничений, ВерОятНо, не своместна')
            raise Incompatible_constraints
        except Iteraions_limit as il:
            showerror("Ошибка",
                      "Зацикливание видимо или ещё где-то прикольчик\n" + "(Или я дурачок, что тоже вероятно)")
            raise il
        except Unlimited_function as ul:
            showerror("Ошибка", "Вероятно неограниченная ЦФ")
            raise ul
        except Exception as e:
            showerror("Ошибка", "неизвестная проблемка какая-то образоваласт")
            raise e
        return Node(res[1], self.allvar, res[2], res[0])


    def find_criteria(self,extremum_value): #Поиск критерия (extremum_value - значение f и переменных на оптимальном решении
        i = 1
        while (
                np.isclose(extremum_value[f'x{i}'],
                           round(extremum_value[f'x{i}'])) if f'x{i}' in extremum_value else True):
            i += 1
        return [f'x{i}', extremum_value[f'x{i}']]



    def print_tree(self, node=None, indent=0):
        """Рекурсивная текстовая визуализация дерева с критерием в начале"""
        if node is None:
            node = self.root
        components = []
        if hasattr(node, 'criteria') and node.criteria:
            components.append(f" Критерий: {node.criteria} | ")
        vars_str = ", ".join(f"{k}={v:.2f}" for k, v in sorted(node.extremum.items())
                             if k in self.allvar or k == 'f')
        components.append(vars_str)
        components.append(f"| ЦФ: {node.extremum.get('f', 0):.2f}")
        if node.integer:
            prefix = " " * indent + "└── ★"
        else:
            prefix = " " * indent + "└── "
        node_line = prefix + "".join(components)
        print(node_line)
        for child in node.children:
            self.print_tree(child, indent + 4)

















