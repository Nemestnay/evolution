# -*- coding: cp1251 -*-
#импортирование библиотек
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#удаление текста в окне
def delete():
    output_text1.delete("0.0", tk.END)
    ax.clear()
    ax1.clear()
    canvas.draw()
    canvas1.draw()

#функция создания популяции
def create():
    global swarm
    global velocity
    global pbest_pos
    global pbest_value
    global gbest_pos
    global gbest_value
    global k
    global bounds
    global mystat
    mystat = []
    ax.clear()
    ax1.clear()
    canvas.draw()
    canvas1.draw()
    k_entry.delete(0, tk.END)
    k_entry.insert(0, 0)
    k = 0
    bounds = np.array([int(minn_entry.get()), int(maxx_entry.get())])
    swarm = np.random.uniform(bounds[0], bounds[1], (int(kolvo_entry.get()), 2))
    velocity = np.zeros((int(kolvo_entry.get()), 2))
    pbest_pos = swarm.copy()
    pbest_value = np.array([np.inf] * int(kolvo_entry.get()))
    gbest_pos = np.zeros(2)
    gbest_value = np.inf

#основная функция
def function(x):
    return 4 * (x[0] - 5) ** 2 + (x[1] - 6) ** 2

#аотображение графиков функции
def draw_graph(points):
    #двумерный график
    ax.clear()
    ax.axis([-100, 100, -100, 100])
    x = [point[0] for point in points]
    y = [point[1] for point in points]
    ax.scatter(x, y)
    canvas.draw()

    #трехмерный график
    ax1.clear()
    z = []
    for i in range(len(points)):
        z.append(function(points[i]))
    ax1.scatter(x, y, z)
    canvas1.draw()


def main():
    global swarm
    global velocity
    global pbest_pos
    global pbest_value
    global gbest_pos
    global gbest_value
    global k
    global bounds
    global mystat
    gener_val = int(generations_var.get())
    kolvo_val = int(kolvo_entry.get())
    k += gener_val
    k_entry.delete(0, tk.END)
    k_entry.insert(0, k)
    w = 0.5
    c1 = c2 = float(speed_entry.get())
    for i in range(gener_val):
        #вычисление значения функции для каждой частицы
        f = np.array([function(x) for x in swarm])

        #обновление лучшей позиции для каждой частицы
        mask = f < pbest_value
        pbest_value[mask] = f[mask]
        pbest_pos[mask] = swarm[mask]

        #обновление лучшей позиции для всего роя
        mask = pbest_value < gbest_value
        if np.any(mask):
            gbest_value = np.min(pbest_value)
            gbest_pos = pbest_pos[np.argmin(pbest_value)]
        if gbest_value < 80 :
            mystat.append(gbest_value)

        r1 = np.random.rand(kolvo_val, 2)
        r2 = np.random.rand(kolvo_val, 2)
        velocity = w * velocity + c1 * r1 * (pbest_pos - swarm) + c2 * r2 * (gbest_pos - swarm)
        swarm = swarm + velocity

         #обрезаем значения позиций частиц до границ пространства поиска
        swarm = np.clip(swarm, bounds[0], bounds[1])

        #заменяем значения, находящиеся за границами, на соответствующие граничные значения
        swarm = np.where(swarm < bounds[0], bounds[0], swarm)
        swarm = np.where(swarm > bounds[1], bounds[1], swarm)
    draw_graph(swarm)
    #отображение текущего состояния поколения
    output_text2.delete(1.0, tk.END)
    output_text2.insert(tk.END, "Номер, Значение, Ген1, Ген2 \n")
    for i in range(kolvo_val):
        line = "{} , {}, {}".format(i,pbest_value[i].round(4), pbest_pos[i].round(4)) + "\n"
        output_text2.insert(tk.END, line)

    resx = "Minimum found: {}".format(gbest_pos.round(6))
    resy = "Minimum value: {}".format(gbest_value.round(6))
    output_text1.insert("1.0", resx + "\n")
    output_text1.insert("1.0", resy + "\n")
    output_text1.insert("1.0", "\n")



#создание окна
root = tk.Tk()
root.title("Роевой алгоритм")
root.geometry("2000x1000")

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


#frame 1
frame1 = ttk.LabelFrame(left_frame, padding=10, text="Параметры")
frame11 = ttk.LabelFrame(left_frame, padding=10, text="Количество шагов")
frame2 = ttk.LabelFrame(left_frame, padding=10, text="Управление")
frame3 = ttk.LabelFrame(left_frame, padding=10, text="Результаты")

frame1.pack(side="top", fill="x", padx=5, pady=5)
frame11.pack(side="top", fill="x", padx=5, pady=5)
frame2.pack(side="top", fill="x", padx=5, pady=5)
frame3.pack(side="top", fill="both", expand=True, padx=5, pady=5)

combo_label = ttk.Label(frame1, text="Функция")
function_label = ttk.Label(frame1, text="4 * (x[0] - 5) ** 2 + (x[1] - 6) ** 2")

kolvo_lable = ttk.Label(frame1, text="Кол-во членов популяции")
kolvo_entry = ttk.Spinbox(frame1, from_=0, to=10000)
kolvo_entry.insert(0, "50")

minn_label = ttk.Label(frame1, text="Минимальное значение гена")
minn_entry = ttk.Spinbox(frame1, from_=-10000, to=10000)
minn_entry.insert(0, "-100")

maxx_label = ttk.Label(frame1, text="Максимальное значение гена")
maxx_entry = ttk.Spinbox(frame1, from_=-10000, to=10000)
maxx_entry.insert(0, "100")


speed_label = ttk.Label(frame1, text="Коэффициент ускорения")
speed_entry = ttk.Spinbox(frame1, from_=-100, to=100)
speed_entry.insert(0, "1.4")


combo_label.grid(row=0, column=0)
function_label.grid(row=0, column=1)

kolvo_lable.grid(row=2, column=0, padx=0, pady=5)
kolvo_entry.grid(row=2, column=1, padx=5, pady=5)

minn_label.grid(row=3, column=0, padx=0, pady=5)
minn_entry.grid(row=3, column=1, padx=5, pady=5)

maxx_label.grid(row=4, column=0, padx=0, pady=5)
maxx_entry.grid(row=4, column=1, padx=5, pady=5)

speed_label.grid(row=5, column=0, padx=0, pady=5)
speed_entry.grid(row=5, column=1, padx=5, pady=5)


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

#frame2
k = 0
create_button = ttk.Button(frame2, text="Создать особей с начальными данными", command=create)
calculate_button = ttk.Button(frame2, text="Посчитать шаги", command=main)
k_label = ttk.Label(frame2, text="Шагов прошло:")
k_entry = ttk.Entry(frame2)
create_button.grid(row=2, column=0, padx=5, pady=5)
calculate_button.grid(row=2, column=1, padx=5, pady=5)
k_label.grid(row=3, column=0, padx=5, pady=5)
k_entry.grid(row=3, column=1, padx=5, pady=5)
output_text1 = ScrolledText(frame3, width=20, height=8)
output_text1.pack(side="top", fill="both", expand=True)
delbutton = ttk.Button(frame3, text="Очистить", command=delete)
delbutton.pack(side="bottom", fill="x")
output_text2 = ScrolledText(middle_frame, width=50, height=53)
output_text2.pack()


bounds = np.array([int(minn_entry.get()) * 2, int(maxx_entry.get()) * 2])
swarm = np.empty((int(kolvo_entry.get()), 2))
velocity = np.empty((int(kolvo_entry.get()), 2))
pbest_pos = swarm.copy()
pbest_value = np.array([np.inf] * int(kolvo_entry.get()))
gbest_pos = np.zeros(2)
gbest_value = np.inf
generations_var.set(1)
mystat = []

#frame 3
figure = Figure(figsize=(4, 4))
ax1= figure.add_subplot(1, 1, 1, projection='3d')
canvas1 = FigureCanvasTkAgg(figure, right_frame)
canvas1.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
canvas1._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
canvas1.mpl_connect('button_press_event', ax1._button_press)
canvas1.mpl_connect('button_release_event', ax1._button_release)
canvas1.mpl_connect('motion_notify_event', ax1._on_move)
canvas1.draw()

fig = Figure(figsize=(4, 4), dpi=100)
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=right_frame)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
root.mainloop()