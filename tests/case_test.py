import json
from src import matrix_utils as mu
from src import branch_bound as bb
from src import math_frame as mf
from src import gomory as gm
import numpy as np



with open('test_cases_ilp.json', 'r') as json_file:
    data = json.load(json_file)

case = data


# matrix_res = mu.create_matr(case['input']['matrix'], case['input']['free'],
#                                case['input']['sign'], case['input']['var'], case['input']['constr'])
# bab = bb.BranchAndBound_method(matrix_res[0], matrix_res[1], matrix_res[2])
# print('Метод ветвей и границ')
# print(bab.error)
# print(bab.finish.extremum)
# bab.print_tree()
#
# print('Гомори')
# gomor = gm.Gomory_method(case['input']['matrix'], case['input']['free'],
#                                case['input']['sign'], case['input']['var'], case['input']['constr'])
#
# print(gomor.extremum)



for case in data:
    matrix_res = mu.create_matr(case['input']['matrix'], case['input']['free'],
                               case['input']['sign'], case['input']['var'], case['input']['constr'])
    bab = bb.BranchAndBound_method(matrix_res[0], matrix_res[1], matrix_res[2])
    gom = gm.Gomory_method(case['input']['matrix'], case['input']['free'],
                               case['input']['sign'], case['input']['var'], case['input']['constr'])
    if bab.error is None:
        res = bab.finish.extremum
        if all((np.isclose(res[sol],case["expected"]["solution"][f'{sol}'])) if sol in res
               else (np.isclose(0,case["expected"]["solution"][f'{sol}']))
               for sol in case["expected"]["solution"]) and np.isclose(res['f'],case["expected"]["objective"]):
            print("\033[32m{}".format(f"test №{case['case_id']} comlited (B&B)"))
        else:
            print("\033[31m{}".format(f"Case №{case['case_id']} error (B&B)"))
            print(res, '\n', case["expected"]["solution"], case["expected"]["objective"])
    else:
        print("\033[31m{}".format(f"Case №{case['case_id']} error (B&B)"))
    if gom.finish:
        res = gom.extremum
        if all((np.isclose(res[sol], case["expected"]["solution"][f'{sol}'])) if sol in res
               else (np.isclose(0, case["expected"]["solution"][f'{sol}']))
               for sol in case["expected"]["solution"]) and np.isclose(res['f'], case["expected"]["objective"]):
            print("\033[32m{}".format(f"test №{case['case_id']} comlited (Gomory)"))
        else:
            print("\033[31m{}".format(f"Case №{case['case_id']} error (Gomory)"))
            print(res, '\n', case["expected"]["solution"], case["expected"]["objective"])
    else:
        print("\033[31m{}".format(f"Case №{case['case_id']} error (Gomory)"))


