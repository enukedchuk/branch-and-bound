import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo
from src import math_frame as mf
from src import branch_bound as bb
from src import matrix_utils as mu
from .exceptions import Incompatible_constraints, Unlimited_function, Iteraions_limit

class MasterClassApp(tk.Tk):
    """Создает корневое окно, инициализирет виджеты и открывает начальный виджет (FirstPage)"""
    def __init__(self):
        super().__init__()
        self.title('Симплекс-метод')
        self.geometry('350x200')
        self.frames = {}
        self.data = {}
        for i in [FirstPage,InputPage]:
            page_name = i.__name__
            frame = i(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame('FirstPage',0,0)

    def show_frame(self,page_name,var,constr):
        """Меняет виджет"""
        frame = self.frames[page_name]
        self.data['var']=int(var)
        self.data['constr']=int(constr)
        if page_name=='InputPage':
            frame.updatik()
        frame.tkraise()


class FirstPage(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        self.controller = controller
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(3, weight=1)
        tk.Label(self, text='Количество переменных').grid(row=1, column=1, sticky='e', padx=5, pady=5)
        tk.Label(self,text='Количество ограничений').grid(row=2, column=1, sticky='e', padx=5, pady=5)
        var_cmb = ttk.Combobox(self, value = [i for i in range(2,11)])
        var_cmb.grid(row=1, column=2, sticky='w', padx=5, pady=5)
        constr_cmb = ttk.Combobox(self, value=[i for i in range(2,11)])
        constr_cmb.grid(row=2, column=2, sticky='w', padx=5, pady=5)
        ttk.Button(self,text='Вперед',command=lambda: controller.show_frame('InputPage', var_cmb.get(), constr_cmb.get())).grid(row=3, column=1, columnspan=2, pady=10)





class InputPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.matrix = []
        self.free = []
        self.var = []
        self.sign = []
        self.direction = tk.IntVar(value=1)
        self.integers_pr = tk.IntVar(value=0)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(100, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        tk.Label(self, text='целевая ФункцИя').grid(row=0, columnspan=10, pady=20,padx=5)
        tk.Label(self, text='ограНичЭнияК').grid(row=3, columnspan=10, pady=20,padx=5)
        tk.Button(self,text='ОпТиМиЗиРоВаТь',command=self.res).grid(row=98, column=0, columnspan=20, pady=10)



    def updatik(self):
        """Добавляет в виджет ячейки и обозначения,
        зависящие от введенных параметров (количество перменных и ограничений)"""
        self.controller.geometry(f'{self.controller.data["var"]*100+340//self.controller.data["var"]}x{self.controller.data["constr"]*int((300//self.controller.data["constr"]**0.75))}')
        self.var = [f'x{i+1}' for i in range(self.controller.data['var'])]
        l = []
        for i in range(int(self.controller.data['var'])):
            tk.Label(self, text=self.var[i]).grid(row=1, column=i, padx=5)
            entry = ttk.Entry(self, width=8)
            entry.grid(row=2, column=i, padx=5)
            l.append(entry)
        self.matrix.append(l)
        tk.Label(self, text='B').grid(row=1, column=self.controller.data['var'], padx=5)
        entry = ttk.Entry(self, width=8)
        entry.grid(row=2, column=self.controller.data['var'], padx=5)
        ttk.Radiobutton(self, text='Min',value=1,variable=self.direction).grid(row=0,column=self.controller.data["var"]+2)
        ttk.Radiobutton(self, text='Max',value=0,variable=self.direction).grid(row=1,column=self.controller.data["var"]+2, padx=20)
        self.free.append(entry)
        for i in range(len(self.var)): tk.Label(self, text=self.var[i]).grid(row=4, column=i, padx=5)
        for i in range(int(self.controller.data['constr'])):
            inter_list = []
            for c in range(int(self.controller.data['var'])):
                entry = ttk.Entry(self, width=8)
                entry.grid(row=5 + i, column=c, padx=5)
                inter_list.append(entry)
            self.matrix.append(inter_list)
            cmb = ttk.Combobox(self,value=['<=','=>','='],width=8)
            cmb.grid(row=5 + i, column=int(self.controller.data['var'])+1, padx=5)
            self.sign.append(cmb)
            tk.Label(self, text='B').grid(row=4, column=int(self.controller.data['var'])+2, padx=5)
            entry = ttk.Entry(self, width=8)
            entry.grid(row=5 + i, column=int(self.controller.data['var'])+2, padx=5)
            self.free.append(entry)
        ttk.Checkbutton(text="Целочисленность", variable=self.integers_pr).grid(row=100)

    def res(self):
        """Собирает данные, вызывает функцию создания матриц/приведения к каноническому виду,
        передает данные в функцию симплекс-метода/метод ветвей и границ и формирует ответ"""
        try:
            matrix = [[float(c.get()) for c in i] for i in self.matrix]
            free = [float(i.get()) for i in self.free]
        except ValueError:
            showerror("Ошибка", "Введите численные значения")
            return 0
        if self.direction.get() == 0:
            matrix[0] = [-i for i in matrix[0]]
            free[0] = -free[0]
        sign = [i.get() for i in self.sign]
        matrix_res = mu.create_matr(matrix, free, sign, self.controller.data['var'],
                                   self.controller.data['constr'])
        if self.integers_pr.get() == 0:
            try:
                res = mf.simplex_method(matrix_res[0], matrix_res[1], matrix_res[2])[0]
                showinfo('Результат', f"f = {res.get('f', 0) * (-1) ** self.direction.get():.2f}\n" +
                         '\n'.join(f"{var} = {res.get(var, 0):.2f}" for var in self.var))
            except Incompatible_constraints:
                showerror('Ошибка', 'Система ограничений, ВерОятНо, не своместна')
            except Iteraions_limit:
                showerror("Ошибка",
                          "Зацикливание видимо или ещё где-то прикольчик\n" + "(Или я дурачок, что тоже вероятно)")
            except Unlimited_function:
                showerror("Ошибка", "Вероятно неограниченная ЦФ")
            except Exception:
                showerror("Ошибка", "неизвестная проблемка какая-то образоваласт")

        else:
            bab = bb.BranchAndBound_method(matrix_res[0], matrix_res[1], matrix_res[2])
            if bab.error is None:
                res = bab.finish.extremum
                showinfo('Результат', f"f = {res.get('f', 0) * (-1) ** self.direction.get():.2f}\n" +
                     '\n'.join(f"{var} = {res.get(var, 0):.2f}" for var in self.var))
                bab.print_tree()
            else:
                showerror('Ошибка', 'Перекрестить можно, чт0-то не работает')
                print(bab.error)

