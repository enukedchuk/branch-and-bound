from src import matrix_utils as mu
from src import math_frame as mf
import numpy as np


class Gomory_method:
    def __init__(self, matrix,free, sign, var, constr):
        matrix_res = mu.create_matr(matrix,free, sign, var, constr)
        res = mf.simplex_method(matrix_res[0], matrix_res[1], matrix_res[2])
        self.matrix = res[1]
        self.allvar = matrix_res[1]
        self.dependend = res[2]
        self.extremum = res[0]
        self.finish = self.solve()

    def solve(self):
        iteration_g_limit=100
        iteration_g = 0
        while iteration_g<iteration_g_limit:
            if all(np.isclose(self.extremum[x], round(self.extremum[x])) for x in self.extremum if x.startswith('x')):
                return True
            list_m = self.matrix[1:,-1]%1
            for i in range(1, len(self.dependend)):
                if 'x' not in self.dependend[i]:
                    list_m[i-1]=0
            index = np.argmax(list_m%1)+1
            matrix = np.vstack([self.matrix,self.matrix[index]%1*-1])
            matrix = np.insert(matrix,len(matrix[0])-1,np.zeros((1,len(matrix)),dtype=float),axis=1)
            matrix[-1,-2]=1
            self.allvar.append(f's{iteration_g}')
            self.dependend.append(f's{iteration_g}')
            result = mf.dual_simplex(matrix,self.allvar,self.dependend)
            self.extremum = result[0]
            self.matrix = result[1]
            self.dependend = result[2]
            iteration_g+=1

