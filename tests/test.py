#Тут ничего нет

import unitest
from src import math_frame as mf


class Math_frame_test(unitest.TestCase):
    def __init__(self):
        pass

    def setUp(self):
        self.simplex_method = mf.simplex_method()
        self.dual_simplex = mf.simplex_method()


