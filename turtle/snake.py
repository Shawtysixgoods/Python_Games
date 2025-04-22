# -*- coding: utf-8 -*-
import turtle
import time
import random

# --- Константы и Переменные ---
DELAY = 0.1          # Задержка в секундах между ходами (контролирует скорость игры)
SCORE = 0            # Текущий счет игрока
HIGH_SCORE = 0       # Лучший счет за сессию
segments = []        # Список для хранения сегментов тела змейки

# --- Настройка Экрана ---
wn = turtle.Screen() # Создаем объект экрана
wn.title("Змейка на Turtle") # Заголовок окна
wn.bgcolor("lightgreen")    # Цвет фона
wn.setup(width=600, height=600) # Размер окна
wn.tracer(0)       # Отключаем автоматическое обновление экрана

# --- Голова Змейки ---
head = turtle.Turtle() # Создаем черепашку для головы
head.speed(0)          # Максимальная скорость анимации (мгновенное перемещение)
head.shape("square")   # Форма головы (квадрат)
head.color("black")    # Цвет головы
head.penup()           # Поднимаем перо (голова не должна рисовать линию)
head.goto(0, 0)        # Начальная позиция в центре экрана
head.direction = "stop" # Начальное направление (стоит на месте)

# --- Еда ---
food = turtle.Turtle()   # Создаем черепашку для еды
food.speed(0)            # Максимальная скорость
food.shape("circle")     # Форма еды (круг)
food.color("red")        # Цвет еды
food.penup()             # Поднимаем перо
food.goto(0, 100)        # Начальная позиция еды

# --- Текст Счета ---
pen = turtle.Turtle()    # Черепашка для отображения текста
pen.speed(0)             # Максимальная скорость
pen.shape("square")      # Форма (невидима)
pen.color("black")       # Цвет текста
pen.penup()              # Поднимаем перо
pen.hideturtle()         # Делаем саму черепашку невидимой
pen.goto(0, 260)         # Позиция текста (вверху экрана)
pen.write("Счет: 0  Рекорд: 0", align="center", font=("Courier", 24, "normal")) # Начальный текст

# --- Функции Движения ---
def go_up():
    """Устанавливает направление движения вверх, если змейка не движется вниз."""
    if head.direction != "down":
        head.direction = "up"

def go_down():
    """Устанавливает направление движения вниз, если змейка не движется вверх."""
    if head.direction != "up":
        head.direction = "down"

def go_left():
    """Устанавливает направление движения влево, если змейка не движется вправо."""
    if head.direction != "right":
        head.direction = "left"

def go_right():
    """Устанавливает направление движения вправо, если змейка не движется влево."""
    if head.direction != "left":
        head.direction = "right"

def move():
    """Перемещает голову змейки на 20 пикселей в текущем направлении."""
    if head.direction == "up":
        y = head.ycor() # Получаем текущую Y координату
        head.sety(y + 20) # Устанавливаем новую Y координату (+20 вверх)

    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20) # Устанавливаем новую Y координату (-20 вниз)

    if head.direction == "left":
        x = head.xcor() # Получаем текущую X координату
        head.setx(x - 20) # Устанавливаем новую X координату (-20 влево)

    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20) # Устанавливаем новую X координату (+20 вправо)

# --- Привязка Клавиш ---
wn.listen() # Начинаем слушать события клавиатуры
wn.onkeypress(go_up, "Up")      # Стрелка вверх -> go_up
wn.onkeypress(go_down, "Down")  # Стрелка вниз -> go_down
wn.onkeypress(go_left, "Left")  # Стрелка влево -> go_left
wn.onkeypress(go_right, "Right")# Стрелка вправо -> go_right
# Можно добавить альтернативные клавиши (W, A, S, D)
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")


# --- Основной Игровой Цикл ---
while True:
    # Обновляем экран на каждой итерации
    wn.update()

    # --- Проверка столкновения с границей ---
    if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
        time.sleep(1) # Пауза перед рестартом
        head.goto(0, 0) # Возвращаем голову в центр
        head.direction = "stop" # Останавливаем движение

        # Скрываем сегменты хвоста (перемещаем за экран)
        for segment in segments:
            segment.goto(1000, 1000)
        segments.clear() # Очищаем список сегментов

        # Сбрасываем счет и задержку
        SCORE = 0
        DELAY = 0.1
        pen.clear() # Очищаем старый текст счета
        pen.write(f"Счет: {SCORE}  Рекорд: {HIGH_SCORE}", align="center", font=("Courier", 24, "normal"))

    # --- Проверка столкновения с едой ---
    # distance() вычисляет расстояние между центрами двух черепашек
    if head.distance(food) < 20: # Если расстояние меньше размера головы+еды
        # Перемещаем еду в случайную позицию
        x = random.randint(-280, 280) # Случайная X в пределах поля (-290+10 до 290-10)
        y = random.randint(-280, 280) # Случайная Y
        food.goto(x, y)

        # Добавляем новый сегмент к змейке
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("grey") # Цвет тела
        new_segment.penup()
        segments.append(new_segment) # Добавляем сегмент в список

        # Увеличиваем скорость (уменьшаем задержку)
        if DELAY > 0.01: # Добавляем предел, чтобы игра не стала невозможной
           DELAY -= 0.002

        # Увеличиваем счет
        SCORE += 10
        if SCORE > HIGH_SCORE: # Обновляем рекорд, если нужно
            HIGH_SCORE = SCORE
        pen.clear() # Очищаем старый счет
        pen.write(f"Счет: {SCORE}  Рекорд: {HIGH_SCORE}", align="center", font=("Courier", 24, "normal")) # Пишем новый

    # --- Перемещение Сегментов Хвоста ---
    # Двигаем сегменты в обратном порядке: последний сегмент перемещается на место предпоследнего, и т.д.
    for index in range(len(segments) - 1, 0, -1): # Идем от предпоследнего к первому
        x = segments[index - 1].xcor() # Координаты предыдущего сегмента
        y = segments[index - 1].ycor()
        segments[index].goto(x, y) # Перемещаем текущий сегмент на место предыдущего

    # Перемещаем первый сегмент (ближайший к голове) на место головы *перед* ее движением
    if len(segments) > 0:
        x = head.xcor() # Текущие координаты головы
        y = head.ycor()
        segments[0].goto(x, y) # Первый сегмент идет туда, где была голова

    # --- Двигаем Голову ---
    move() # Вызываем функцию перемещения головы

    # --- Проверка столкновения Головы с Телом ---
    for segment in segments:
        if segment.distance(head) < 20: # Если голова столкнулась с сегментом хвоста
            time.sleep(1) # Пауза
            head.goto(0, 0) # Рестарт
            head.direction = "stop"
            # Скрыть сегменты
            for seg in segments:
                seg.goto(1000, 1000)
            segments.clear()
            SCORE = 0
            DELAY = 0.1
            pen.clear()
            pen.write(f"Счет: {SCORE}  Рекорд: {HIGH_SCORE}", align="center", font=("Courier", 24, "normal"))
            # Прерываем цикл проверки столкновений с телом после первого обнаружения
            break 

    # --- Пауза ---
    time.sleep(DELAY) # Ждем перед следующей итерацией цикла

# Эта строка обычно не достигается в играх с бесконечным циклом,
# но нужна, если бы цикл мог завершиться.
# wn.mainloop()
