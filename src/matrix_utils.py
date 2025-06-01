import numpy as np

def create_matr(constraint_matrix, free, sign, var, constr):
    """Создание и приведение к каноническому виду матриц + метод штрафов (если требуется)
    Параметры:
    constraint_matrix - матрица коэффициентов ц.ф. + ограничений (list)
    free - список свободных членов
    sign - список знаков ограничений
    var - количество перменных
    constr - количество ограничений

    На выходе:
    [Матрица, список переменных по порядку, список зависимых переменных по порядку]"""

    penalty= 10**(len(str(int(abs(np.max(constraint_matrix)))))+2)
    all = [f'x{i+1}' for i in range(var)]
    dependent = ['f']
    constraint_matrix = np.array(constraint_matrix,dtype=float)
    r = np.zeros((constraint_matrix.shape[0], 0))
    free = np.array(free)

    for i in range(constr):
        if sign[i]=='<=':
            all.append(f'y{i+1}')
            if free[i+1]>=0:
                dependent.append(f'y{i+1}')
                constraint_matrix = np.hstack([constraint_matrix,np.zeros((constraint_matrix.shape[0], 1))])
                constraint_matrix[i+1,var+i]=1

            if free[i+1]<0:
                constraint_matrix[i + 1] = constraint_matrix[i + 1] * (-1)
                free[i + 1] = free[i + 1] * (-1)
                sign[i] = '=>'
                constraint_matrix = np.hstack([constraint_matrix, np.zeros((constraint_matrix.shape[0], 1))])
                constraint_matrix[i + 1, var + i] = -1
                r = np.hstack([r, np.zeros((constraint_matrix.shape[0], 1))])
                r[i + 1, -1] = 1
                dependent.append(f'r{i + 1}')
                continue

        if sign[i]=='=>':
            all.append(f'y{i + 1}')
            if free[i+1]<=0:
                constraint_matrix[i + 1] = constraint_matrix[i + 1] * (-1)
                free[i+1] = free[i+1]*(-1)
                sign[i] = '<='
                constraint_matrix = np.hstack([constraint_matrix, np.zeros((constraint_matrix.shape[0], 1))])
                constraint_matrix[i + 1, var + i] = 1
                dependent.append(f'y{i + 1}')
                continue

            if free[i+1]>0:
                constraint_matrix = np.hstack([constraint_matrix, np.zeros((constraint_matrix.shape[0], 1))])
                constraint_matrix[i + 1, var + i] = -1
                r = np.hstack([r, np.zeros((constraint_matrix.shape[0], 1))])
                r[i + 1, -1] = 1
                dependent.append(f'r{i + 1}')

        if sign[i]=='=':
            r = np.hstack([r,np.zeros((constraint_matrix.shape[0], 1))])
            r[i+1,-1]=1
            if free[i + 1] < 0:
                constraint_matrix[i+1]=constraint_matrix[i+1]*(-1)
                free[i + 1] = free[i + 1] * (-1)
            dependent.append(f'r{i + 1}')
            var-=1
    for i in range(len(sign)): #М-метод
        if sign[i] == '=>' or sign[i] == '=':
            constraint_matrix[0] = constraint_matrix[0] - penalty * constraint_matrix[i + 1]
            free[0] = free[0] - penalty * free[i + 1]
    all = all + [var for var in dependent if var.startswith('r')]
    matrix = np.hstack([constraint_matrix, r,free.reshape(-1, 1)])
    return [matrix,all,dependent]

def adding_restrictions(matrix, restr,all_var,dependent_var):
    """Добавление ограниченйи в решение для двойственного симплекс-метода

    Параметры:
    matrix - матрица решения
    restr - вводимое ограничение ([Переменная, значение])
    all_var - все перменные по порядку
    dependent_var - базисные переменные по порядку

    На выходе:
    Матрица с ограничением (переменная <= значения), матрица с ограничение (переменная >= значение), все переменные, базисные переменные"""

    matrix = np.insert(matrix, len(matrix[0]) - 1, np.zeros((1, len(matrix)), dtype=float), axis=1)
    new_str = np.zeros((1, len(matrix[0])), dtype=float)
    new_str[0, all_var.index(restr[0])], new_str[0, len(matrix[0]) - 2], new_str[0, len(matrix[0]) - 1] = 1, 1, \
        restr[1] // 1
    new_str1 = new_str - matrix[dependent_var.index(restr[0])]
    matrix1 = np.vstack([matrix, new_str1])
    new_str[0, len(matrix[0]) - 2], new_str[0, len(matrix[0]) - 1] = -1, restr[1] // 1 + 1
    new_str2 = -new_str + matrix[dependent_var.index(restr[0])]
    matrix2 = np.vstack([matrix, new_str2])
    all_var.append(f'y{sum(x.startswith("y") for x in all_var) + 1}')
    dependent_var.append(f'y{sum(x.startswith("y") for x in all_var)}')
    return matrix1, matrix2, all_var,dependent_var

