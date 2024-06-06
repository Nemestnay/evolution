# импортирование библиотек
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import random
import matplotlib.pyplot as plt
import tkinter as tk
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

#удаление текста в окне
def delete():
    output_text1.delete("0.0", tk.END)
    plt.cla()


#основная функция
def function(x):
    func = combo.get()
    return 4 * (x[0] - 5) ** 2 + (x[1] - 6) ** 2

#функция создания популяции
def create():
    k_entry.delete(0, tk.END)
    k_entry.insert(0,0)
    global mypop
    global mystat
    global k
    k = 0
    mypop = [generate_child() for i in range(int(kolvo_entry.get()))]
    mystat = []

#функция создания ребенка
def generate_child():
    child = []
    minn = int(minn_entry.get())
    maxx = int(maxx_entry.get())
    child.append(random.uniform(minn, maxx))
    child.append(random.uniform(minn, maxx))
    return child


#функция рождения нового ребенка от двух родителей
def birthday(parent1, parent2):
    child = []
    child.append((parent1[0] + parent2[0]) / 2)
    child.append((parent1[1] + parent2[1]) / 2)
    return child


#функция мутации новой особи
def mutation(child):
    child[0] += random.uniform(-0.5, 0.5)
    child[1] += random.uniform(-0.5, 0.5)
    return child

#функция кроссинговера для новой особи
def krossingover(child):
    t = child[0]
    child[0] = child[1]
    child[1] += t
    return child



def main():
    global k
    k += int(generations_var.get())
    k_entry.delete(0, tk.END)
    k_entry.insert(0,k)
    #смена поколений
    for generation in range(int(generations_var.get())):
        function_score = [function(child) for child in mypop]
        parents = random.choices(mypop, weights=function_score, k=2)
        kid = birthday(parents[0], parents[1])
        mutpercent = int(mutant_entry.get()) / 100
        krospercent = int(kros_entry.get()) / 100
        kolvo = int(kros_entry.get())
        #мутация особи
        aaa = random.random()
        if  aaa < mutpercent:
            kid = mutation(kid)
        #кроссинговер особи
        #aaa = random.random()
        aaa = 1
        if krospercent > aaa:
            kid = krossingover(kid)
        delete_index = function_score.index(max(function_score))
        mypop[delete_index] = kid
        best_child = min(mypop, key=function)
        best_val = round(function(best_child), 2)
        if best_val<0.5:
            mystat.append(best_val)
    #запись в окно нового поколения
    output_text2.delete(1.0, tk.END)
    output_text2.insert(tk.END, "Номер, Значение, Ген1, Ген2 \n")
    for i in range(len(function_score)):
        line = "{},     {},   {},   {}".format(i, round(function_score[i], 2), round(mypop[i][0], 2),
                                        round(mypop[i][1], 2)) + "\n"
        output_text2.insert(tk.END, line)

    #запись в окно лучшего найденнго найденного решения
    best_child = min(mypop, key=function)
    resx = "Minimum found: {}, {}".format(round(best_child[0], 2), round(best_child[1], 2))
    resy = "Minimum value: {}".format(round(function(best_child), 2))
    output_text1.insert("1.0", resx + "\n")
    output_text1.insert("1.0", resy + "\n")
    output_text1.insert("1.0", " \n")


#создание окна
root = tk.Tk()
root.title("Генетический алгоритм")
root.geometry("2000x800")

#создание трех полей
left_frame = ttk.Frame(root, padding=10)
middle_frame = ttk.LabelFrame(root, padding=10, text="Хромосомы поколения")
right_frame = ttk.LabelFrame(root, padding=10, text="График функции")

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)

left_frame.grid(row=0, column=0, sticky="nsew")
middle_frame.grid(row=0, column=1, sticky="nsew")
right_frame.grid(row=0, column=2, sticky="nsew")


#frame1
frame1 = ttk.LabelFrame(left_frame, padding=10, text="Параметры")
frame11 = ttk.LabelFrame(left_frame, padding=10, text="Количество шагов")
frame2 = ttk.LabelFrame(left_frame, padding=10, text="Управление")
frame3 = ttk.LabelFrame(left_frame, padding=10, text="Результаты")

frame1.pack(side="top", fill="x", padx=5, pady=5)
frame11.pack(side="top", fill="x", padx=5, pady=5)
frame2.pack(side="top", fill="x", padx=5, pady=5)
frame3.pack(side="top", fill="both", expand=True, padx=5, pady=5)

combo_label = ttk.Label(frame1, text="Функция")
combo = ttk.Combobox(frame1, width="40")
combo['value'] = ("4*(x[0] - 5)**2 + (x[1] - 6)**2",)
combo.current(0)

mutant_label = ttk.Label(frame1, text="Вероятность мутации")
mutant_entry = ttk.Spinbox(frame1, from_=0, to=100)
mutant_entry.insert(0, "10")
kros_lable = ttk.Label(frame1, text="Вероятность кроссинговера")
kros_entry = ttk.Spinbox(frame1, from_=0, to=100)
kros_entry.insert(0, "10")
kolvo_label = ttk.Label(frame1, text="Кол-во членов популяции")
kolvo_entry = ttk.Spinbox(frame1, from_=0, to=10000)
kolvo_entry.insert(0, "50")
minn_label = ttk.Label(frame1, text="Минимальное значение гена")
minn_entry = ttk.Spinbox(frame1, from_=-10000, to=10000)
minn_entry.insert(0, "-50")
maxx_label = ttk.Label(frame1, text="Максимальное значение гена")
maxx_entry = ttk.Spinbox(frame1, from_=-10000, to=10000)
maxx_entry.insert(0, "50")

combo_label.grid(row=0, column=0)
combo.grid(row=1, column=0)

mutant_label.grid(row=2, column=0, padx=0, pady=5)
mutant_entry.grid(row=2, column=1, padx=5, pady=5)

kros_lable.grid(row=3, column=0, padx=0, pady=5)
kros_entry.grid(row=3, column=1, padx=5, pady=5)

kolvo_label.grid(row=4, column=0, padx=0, pady=5)
kolvo_entry.grid(row=4, column=1, padx=5, pady=5)

minn_label.grid(row=5, column=0, padx=0, pady=5)
minn_entry.grid(row=5, column=1, padx=5, pady=5)

maxx_label.grid(row=6, column=0, padx=0, pady=5)
maxx_entry.grid(row=6, column=1, padx=5, pady=5)

generations_var = tk.IntVar()
spin = ttk.Spinbox(frame11, from_=10, to=1000, width=10, textvariable=generations_var)
radio_button0 = ttk.Radiobutton(frame11, text="1", variable=generations_var, value=1)
radio_button1 = ttk.Radiobutton(frame11, text="10", variable=generations_var, value=10)
radio_button2 = ttk.Radiobutton(frame11, text="100", variable=generations_var, value=100)
radio_button3 = ttk.Radiobutton(frame11, text="500", variable=generations_var, value=500)

radio_button0.grid(row=0, column=0, padx=1, pady=5)
radio_button1.grid(row=0, column=1, padx=1, pady=5)
radio_button2.grid(row=0, column=2, padx=1, pady=5)
radio_button3.grid(row=0, column=3, padx=1, pady=5)
spin.grid(row=0, column=4, padx=5, pady=5)

# frame2
k = 0
create_button = ttk.Button(frame2, text="Заполнить хромосомы начальными данными", command=create)
calculate_button = ttk.Button(frame2, text="Посчитать все шаги", command=main)
k_label = ttk.Label(frame2,text="Шагов прошло:")
k_entry = ttk.Entry(frame2)
create_button.grid(row=2, column=0, padx=5, pady=5)
calculate_button.grid(row=2, column=1, padx=5, pady=5)
k_label.grid(row=3,column=0,padx=5, pady=5)
k_entry.grid(row=3,column=1,padx=5, pady=5)
output_text1 = ScrolledText(frame3, width=20, height=8)
output_text1.pack(side="top", fill="both", expand=True)
delbutton = ttk.Button(frame3, text="Очистить", command=delete)
delbutton.pack(side="bottom", fill="x")
output_text2 = ScrolledText(middle_frame, width=50, height=35)
output_text2.pack(side="left", fill="both", expand=True)



mypop = []
mystat = []
generations_var.set(1)

#frame 3
x=np.linspace(-50, 50, 100)
y=np.linspace(-50, 50, 100)
X, Y = np.meshgrid(x, y)
Z = function([X, Y])


figure = Figure(figsize=(4, 4))
ax= figure.add_subplot(1, 1, 1, projection='3d')
ax.plot_surface(X, Y, Z, shade=True)
canvas = FigureCanvasTkAgg(figure, right_frame)
canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
canvas.mpl_connect('button_press_event', ax._button_press)
canvas.mpl_connect('button_release_event', ax._button_release)
canvas.mpl_connect('motion_notify_event', ax._on_move)
canvas.draw()



root.mainloop()