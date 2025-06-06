import turtle  # Импортируем библиотеку turtle для рисования

# Настройка окна и черепахи
screen = turtle.Screen()  # Создаем экран для рисования
screen.bgcolor("white")  # Устанавливаем белый цвет фона
t = turtle.Turtle()  # Создаем черепаху для рисования
t.speed(3)  # Устанавливаем скорость рисования

# Функция для рисования квадрата
def draw_square(size):  # Определяем функцию для рисования квадрата
    for _ in range(4):  # Повторяем 4 раза для рисования четырех сторон квадрата
        t.forward(size)  # Двигаемся вперед на заданное расстояние (размер квадрата)
        t.left(90)  # Поворот на 90 градусов

# Функция для рисования треугольника
def draw_triangle(size):  # Определяем функцию для рисования треугольника
    for _ in range(3):  # Повторяем 3 раза для рисования трех сторон треугольника
        t.forward(size)  # Двигаемся вперед на заданное расстояние (размер треугольника)
        t.left(120)  # Поворот на 120 градусов (угол треугольника)

# Рисуем квадрат для дома
t.penup()  # Поднимаем перо, чтобы не рисовать линии при перемещении
t.goto(-100, -100)  # Перемещаем черепаху в точку (-100, -100)
t.pendown()  # Опускаем перо, чтобы начать рисовать
draw_square(200)  # Рисуем квадрат размером 200x200

# Рисуем крышу (треугольник)
t.penup()  # Поднимаем перо, чтобы не рисовать линии при перемещении
t.goto(-120, 100)  # Перемещаем черепаху в точку (-120, 100) для начала рисования крыши
t.pendown()  # Опускаем перо, чтобы начать рисовать
draw_triangle(240)  # Рисуем треугольник (крышу) размером 240x240

# Рисуем окна (два квадрата)
t.penup()  # Поднимаем перо, чтобы не рисовать линии при перемещении
t.goto(-70, 20)  # Перемещаем черепаху в точку (-70, 20) для первого окна
t.pendown()  # Опускаем перо, чтобы начать рисовать
draw_square(40)  # Рисуем квадрат окна размером 40x40

t.penup()  # Поднимаем перо, чтобы не рисовать линии при перемещении
t.goto(30, 20)  # Перемещаем черепаху в точку (30, 20) для второго окна
t.pendown()  # Опускаем перо, чтобы начать рисовать
draw_square(40)  # Рисуем второй квадрат окна размером 40x40

# Рисуем дверь (прямоугольник)
t.penup()  # Поднимаем перо, чтобы не рисовать линии при перемещении
t.goto(-30, -100)  # Перемещаем черепаху в точку (-30, -100) для двери
t.pendown()  # Опускаем перо, чтобы начать рисовать
t.setheading(0)  # Направляем черепаху вправо (по оси X)
for _ in range(2):  # Рисуем прямоугольник, повторяя 2 раза
    t.forward(60)  # Рисуем одну сторону (дверь)
    t.left(90)  # Поворот на 90 градусов
    t.forward(120)  # Рисуем вторую сторону (высоту двери)
    t.left(90)  # Поворот на 90 градусов

# Завершаем рисование
t.hideturtle()  # Прячем черепаху (курсор), чтобы не мешала
screen.mainloop()  # Оставляем окно открытым до тех пор, пока не будет закрыто вручную
