# -*- coding: utf-8 -*-
import turtle
import time
import random

# --- Константы ---
WIDTH, HEIGHT = 600, 600
DELAY = 0.1 # Задержка для контроля скорости
FOOD_SIZE = 0.8 # Множитель размера (0.8 * 20px = 16px)
SEGMENT_SIZE = 20 # Размер сегмента и шаг движения

# --- Класс Змейки ---
class Snake:
    def __init__(self):
        self.segments = [] # Список черепашек-сегментов
        self.head = self._create_segment(0, 0) # Голова - первый сегмент
        self.head.color("black", "darkgrey") # Отличительный цвет головы
        self.direction = "stop" # Начальное направление
        self.create_initial_snake()

    def _create_segment(self, x, y):
        """Вспомогательный метод для создания сегмента"""
        segment = turtle.Turtle()
        segment.speed(0)
        segment.shape("square")
        segment.color("grey")
        segment.penup()
        segment.goto(x, y)
        return segment

    def create_initial_snake(self):
        """Создает начальную змейку из 3 сегментов"""
        self.head = self._create_segment(0, 0)
        self.head.color("black", "darkgrey")
        self.segments.append(self.head)
        self.grow() # Добавляем еще 2 сегмента для начальной длины
        self.grow()

    def move(self):
        """Двигает змейку"""
        # Двигаем хвост вперед (от предпоследнего к первому)
        for index in range(len(self.segments) - 1, 0, -1):
            x = self.segments[index - 1].xcor()
            y = self.segments[index - 1].ycor()
            self.segments[index].goto(x, y)

        # Двигаем голову
        if self.direction == "up":
            self.head.sety(self.head.ycor() + SEGMENT_SIZE)
        if self.direction == "down":
            self.head.sety(self.head.ycor() - SEGMENT_SIZE)
        if self.direction == "left":
            self.head.setx(self.head.xcor() - SEGMENT_SIZE)
        if self.direction == "right":
            self.head.setx(self.head.xcor() + SEGMENT_SIZE)

    def grow(self):
        """Добавляет сегмент к змейке"""
        new_segment = self._create_segment(self.head.xcor(), self.head.ycor()) # Создаем там же где голова пока
        self.segments.append(new_segment)

    # --- Методы для изменения направления ---
    def go_up(self):
        if self.direction != "down": self.direction = "up"
    def go_down(self):
        if self.direction != "up": self.direction = "down"
    def go_left(self):
        if self.direction != "right": self.direction = "left"
    def go_right(self):
        if self.direction != "left": self.direction = "right"

    def check_collision_wall(self):
        """Проверка столкновения с границами экрана"""
        x, y = self.head.xcor(), self.head.ycor()
        half_w, half_h = WIDTH / 2, HEIGHT / 2
        return x > half_w - SEGMENT_SIZE or x < -half_w + SEGMENT_SIZE or \
               y > half_h - SEGMENT_SIZE or y < -half_h + SEGMENT_SIZE

    def check_collision_self(self):
        """Проверка столкновения головы с телом"""
        for segment in self.segments[1:]: # Проверяем все сегменты кроме головы
            if self.head.distance(segment) < SEGMENT_SIZE / 2:
                return True
        return False

    def reset(self):
        """Сброс змейки в начальное состояние"""
        # Перемещаем все сегменты за экран перед удалением
        for segment in self.segments:
            segment.goto(1000, 1000)
        self.segments.clear()
        self.create_initial_snake() # Создаем змейку заново
        self.direction = "stop"

# --- Класс Еды ---
class Food(turtle.Turtle): # Наследуем от Turtle для простоты
    def __init__(self):
        super().__init__() # Вызываем конструктор родительского класса Turtle
        self.speed(0)
        self.shape("circle")
        self.shapesize(stretch_len=FOOD_SIZE, stretch_wid=FOOD_SIZE) # Уменьшаем размер
        self.color("red")
        self.penup()
        self.refresh() # Размещаем еду сразу при создании

    def refresh(self):
        """Перемещает еду в случайное место"""
        max_x = WIDTH / 2 - SEGMENT_SIZE
        max_y = HEIGHT / 2 - SEGMENT_SIZE
        # Генерируем координаты, кратные размеру сегмента, чтобы еда была на сетке
        x = random.randrange(-max_x, max_x, SEGMENT_SIZE)
        y = random.randrange(-max_y, max_y, SEGMENT_SIZE)
        self.goto(x, y)

# --- Класс Счета ---
class Scoreboard(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.high_score = 0 # Можно добавить сохранение рекорда в файл
        self.color("black")
        self.penup()
        self.hideturtle()
        self.goto(0, HEIGHT / 2 - 40) # Позиция сверху
        self.update_scoreboard()

    def update_scoreboard(self):
        """Обновляет текст счета"""
        self.clear()
        self.write(f"Счет: {self.score}  Рекорд: {self.high_score}", align="center", font=("Courier", 20, "normal"))

    def increase_score(self):
        """Увеличивает счет и обновляет рекорд, если нужно"""
        self.score += 10
        if self.score > self.high_score:
            self.high_score = self.score
        self.update_scoreboard()

    def reset(self):
        """Сбрасывает текущий счет и обновляет текст"""
        self.score = 0
        self.update_scoreboard()

# --- Настройка Экрана ---
screen = turtle.Screen()
screen.setup(width=WIDTH, height=HEIGHT)
screen.bgcolor("lightgreen")
screen.title("Змейка на Turtle (ООП)")
screen.tracer(0) # Отключаем авто-обновление

# --- Создание Объектов ---
snake = Snake()
food = Food()
scoreboard = Scoreboard()

# --- Привязка Клавиш ---
screen.listen()
screen.onkeypress(snake.go_up, "Up")
screen.onkeypress(snake.go_down, "Down")
screen.onkeypress(snake.go_left, "Left")
screen.onkeypress(snake.go_right, "Right")
screen.onkeypress(snake.go_up, "w")
screen.onkeypress(snake.go_down, "s")
screen.onkeypress(snake.go_left, "a")
screen.onkeypress(snake.go_right, "d")

# --- Основной Игровой Цикл ---
game_is_on = True
while game_is_on:
    screen.update() # Обновляем экран
    time.sleep(DELAY) # Пауза

    snake.move() # Двигаем змейку

    # 1. Обнаружение столкновения с едой
    if snake.head.distance(food) < SEGMENT_SIZE:
        food.refresh()
        snake.grow()
        scoreboard.increase_score()
        # Можно добавить ускорение игры
        # DELAY *= 0.98

    # 2. Обнаружение столкновения со стеной
    if snake.check_collision_wall():
        scoreboard.reset()
        snake.reset()
        # DELAY = 0.1 # Сброс скорости

    # 3. Обнаружение столкновения с хвостом
    if snake.check_collision_self():
        scoreboard.reset()
        snake.reset()
        # DELAY = 0.1

# screen.exitonclick() # Можно использовать вместо mainloop, если цикл может завершиться
screen.mainloop()