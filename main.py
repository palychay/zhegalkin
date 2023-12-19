from tkinter import *
from tkinter.messagebox import showerror
from tkinter import filedialog
import itertools

# создание таблицы истинности по введеннеой логической фцнкции
def truth_table(expression):
    variables = set()
    # Находим все уникальные переменные в выражении
    for char in expression:
        if char.isalpha() and (char == 'x' or char == 'y' or char == 'z'):
            variables.add(char)
    
    # Создаем все возможные комбинации значений переменных
    truth_values = list(itertools.product([0, 1], repeat=len(sorted(variables))))

    # Строим таблицу истинности
    truth_table = []
    for values in truth_values:
        row = list(values)
        # Заменяем переменные в выражении на их значения в данной строке
        substitutions = {var: val for var, val in zip(sorted(variables), values)}
        result = eval(expression, substitutions)
        row.append(int(result))
        truth_table.append(row)

    return truth_table

# класс строящий полином жегалкина
class PolynomZhegalkina:
    def __init__(self, matrix):
        self.matrix = matrix
        self.n = len(self.matrix[0]) - 1

    #транспонируем таблицу, потому что нам нужны вектора x1, x2 и тд, а также вектор значений функций
    def create_vector(self):
        art = [[0] * len(self.matrix) for _ in range(len(self.matrix[0]))]
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                art[j][i] = self.matrix[i][j]
        return art
    
    #алгоритм треугольник Паскаля
    def treygolnikPascal(self): 
        self.vector_f = self.create_vector()[-1]
        vector_koef = [self.vector_f[0]]
        nnn = 2**self.n
        vector_new_vector = [self.vector_f]
        for _ in range(2**self.n-1):
            new_vector = []
            for j in range(0, nnn-1):
                new_vector.append(self.vector_f[j] ^ self.vector_f[j+1])
            vector_koef.append(new_vector[0])
            
            self.vector_f = new_vector
            nnn = len(new_vector)
            vector_new_vector.append(new_vector)
        return (vector_koef, vector_new_vector)
    
    #создание полинома
    def create_polynom(self):
        polinom = []
        for i in range(len(self.matrix)):
            if self.treygolnikPascal()[0][i] == 1:
                s = ""
                k = 0
                for j in range(len(self.matrix[0]) - 1):
                    if self.matrix[i][j] == 1:
                        s += f"x{j+1}"
                        k += 1
                if (k == 0):
                    s = '1'
                polinom.append(f"{s} +")
        s = " ".join(polinom)
        s = s[:-2]
        return s
    

class Window:
    def __init__(self, root):
        #создаем окно
        self.root = root
        self.root.geometry('810x200')
        self.root.title('Полином Жегалкина. Павлов АС-22-05')
        self.root['bg'] = 'azure'
        #меню
        main_menu = Menu()
        file_menu = Menu()
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Open", command=self.load_from_file)
        main_menu.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=main_menu)
        #виджеты
        opisanie_alphabet = Label(root, text="!!! Алфавит: x(в ответе 'x1'),\n y(в ответе 'x1' если в функции только y и z, иначе 'x2'),\n z(в ответе 'x2' если в функции только x и z или y и z, иначе 'x3'),\n and - конъюнкция, or - дизъюнкция, == - эквивалентность,\n (not 'ваше выражение') - отрицание !!!", bg='cyan', font="Arial 13")
        opisanie_alphabet.place(x=0, y=50)
        opisanie_vvoda = Label(root, text="Введите функцию",  bg='cyan', font="Arial 15")
        opisanie_vvoda.place(x=0, y=10)
        self.input_function = Entry(root, font='Arial 15', width=30, bg='khaki')
        self.input_function.place(x=176, y=10)
        button_create_polynom = Button(root, text="Построить полином Жегалкина", command=self.polynom, bg='hot pink', font='Arial 13')
        button_create_polynom.place(x=540, y=10)
        button_clear = Button(root, text="Очистить ввод и ответ", command=self.clear, bg='hot pink', font="Arial 13", width=27)
        button_clear.place(x=540, y=50)

    #функция, которая считывает введенную функцию
    def get_function(self):
        function = self.input_function.get()
        return function
    
    #создание таблицы истинности для заданной функции
    def make_truth_table(self):
        table = truth_table(self.get_function())
        return table
    
    #создание полинома
    def polynom(self):
        try:
            self.plo = PolynomZhegalkina(self.make_truth_table())
            self.otvet_label = Label(root, text='Получившийся полином: ', bg='khaki', font='Arial, 15')
            self.otvet_label.place(x=10, y=170)
            self.polynom_label = Label(root, text=str(self.plo.create_polynom()), bg='khaki', font='Arial, 15')
            self.polynom_label.place(x=234, y=170)
            self.anim()

        except:
            showerror(title="Неверный алфавит!", message="Сообщение об ошибке")

    #вывод отдельным окном таблицы истинности и треугольника Паскаля
    def anim(self):
        
        animation = Tk()
        nt = Label(animation, text="Таблица истинности")
        nt.grid(row=0, column=0)
        rtk = 1
        for t in self.make_truth_table():
            newLabel = Label(animation, text=str(t))
            newLabel.grid(row=rtk, column=0)
            rtk += 1

        ntr = Label(animation, text="Треугольник Паскаля")
        ntr.grid(row=0, column=5)
        rtk = 1
        for p in self.plo.treygolnikPascal()[1]:
            newlabel = Label(animation, text=str(p))
            newlabel.grid(row=rtk, column=5)
            rtk += 1

        animation.mainloop()
    
    #очистка виджетов
    def clear(self):
        try:
            self.input_function.delete(0, 'end')
            self.polynom_label.destroy()
            self.otvet_label.destroy()
            self.plo.clear_polynom()
        except:
            pass

    #сохранение файла
    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        try:
            with open(file_path, 'w') as file:
                file.write(self.get_function() + '\n')
                try:
                    file.write("Получившийся полином: ")
                    file.write(self.plo.create_polynom() + '\n')
                    file.write("Таблица истинности\n")
                    rtk = 1
                    for t in self.make_truth_table():
                        file.write(str(t) + '\n')
                        rtk += 1
                    file.write("Треугольник Паскаля\n")
                    for p in self.plo.treygolnikPascal()[1]:
                        file.write(str(p) + '\n')
                        rtk += 1
                except:
                    pass

        except IOError:
            pass

    #загрузка файла
    def load_from_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        try:
            with open(file_path, 'r') as file:
                loaded_text = file.readline()
                self.input_function.insert(0, loaded_text)
        except IOError:
            pass


root = Tk()
win = Window(root)
root.mainloop()