# -*- coding: utf-8 -*-
import turtle
import time

# --- Константы ---
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH = 5  # Множитель ширины (5 * 20px = 100px)
PADDLE_HEIGHT = 1 # Множитель высоты (1 * 20px = 20px)
PADDLE_SPEED = 30 # Скорость движения ракетки
BALL_SPEED_X = 0.2 # Начальная скорость мяча по X
BALL_SPEED_Y = 0.2 # Начальная скорость мяча по Y
SPEED_INCREASE = 1.1 # Множитель увеличения скорости мяча при отскоке

# --- Класс Ракетки ---
class Paddle(turtle.Turtle):
    def __init__(self, position): # position будет (-350, 0) или (350, 0)
        super().__init__()
        self.shape("square")
        self.color("white")
        self.shapesize(stretch_wid=PADDLE_WIDTH, stretch_len=PADDLE_HEIGHT)
        self.penup()
        self.speed(0)
        self.goto(position)

    def go_up(self):
        """Двигает ракетку вверх с ограничением"""
        new_y = self.ycor() + PADDLE_SPEED
        if new_y < (HEIGHT / 2 - PADDLE_WIDTH * 10 / 2): # Ограничение по верху
             self.sety(new_y)

    def go_down(self):
        """Двигает ракетку вниз с ограничением"""
        new_y = self.ycor() - PADDLE_SPEED
        if new_y > (-HEIGHT / 2 + PADDLE_WIDTH * 10 / 2): # Ограничение по низу
            self.sety(new_y)

# --- Класс Мяча ---
class Ball(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        self.color("white")
        self.penup()
        self.speed(0)
        self.goto(0, 0)
        self.dx = BALL_SPEED_X # Начальное смещение по X
        self.dy = BALL_SPEED_Y # Начальное смещение по Y

    def move(self):
        """Перемещает мяч на dx, dy"""
        self.setx(self.xcor() + self.dx)
        self.sety(self.ycor() + self.dy)

    def bounce_y(self):
        """Меняет вертикальное направление"""
        self.dy *= -1

    def bounce_x(self):
        """Меняет горизонтальное направление и немного ускоряет мяч"""
        self.dx *= -SPEED_INCREASE
        self.dy *= SPEED_INCREASE # Ускоряем и по Y для интереса
        # Ограничение максимальной скорости (опционально)
        self.dx = max(min(self.dx, 2), -2)
        self.dy = max(min(self.dy, 2), -2)


    def reset_position(self):
        """Возвращает мяч в центр и меняет направление подачи"""
        self.goto(0, 0)
        self.dx = BALL_SPEED_X * (-1 if self.dx > 0 else 1) # Подача в сторону проигравшего
        self.dy = BALL_SPEED_Y * random.choice([1, -1]) # Случайное направление Y при подаче
        # Сбрасываем ускорение
        self.dx = BALL_SPEED_X if self.dx > 0 else -BALL_SPEED_X
        self.dy = BALL_SPEED_Y if self.dy > 0 else -BALL_SPEED_Y


# --- Класс Счета для Понга ---
class PongScoreboard(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.l_score = 0
        self.r_score = 0
        self.update_scoreboard()

    def update_scoreboard(self):
        """Обновляет текст счета для обоих игроков"""
        self.clear()
        self.goto(-100, HEIGHT / 2 - 50)
        self.write(self.l_score, align="center", font=("Courier", 36, "normal"))
        self.goto(100, HEIGHT / 2 - 50)
        self.write(self.r_score, align="center", font=("Courier", 36, "normal"))

    def l_point(self):
        """Добавляет очко левому игроку"""
        self.l_score += 1
        self.update_scoreboard()

    def r_point(self):
        """Добавляет очко правому игроку"""
        self.r_score += 1
        self.update_scoreboard()

# --- Настройка Экрана ---
screen = turtle.Screen()
screen.setup(width=WIDTH, height=HEIGHT)
screen.bgcolor("black")
screen.title("Понг на Turtle (ООП)")
screen.tracer(0)

# --- Создание Объектов ---
r_paddle = Paddle((WIDTH/2 - 50, 0))  # Правая ракетка
l_paddle = Paddle((-WIDTH/2 + 50, 0)) # Левая ракетка
ball = Ball()
scoreboard = PongScoreboard()

# --- Привязка Клавиш ---
screen.listen()
# Левая ракетка (W/S)
screen.onkeypress(l_paddle.go_up, "w")
screen.onkeypress(l_paddle.go_down, "s")
# Правая ракетка (Стрелки)
screen.onkeypress(r_paddle.go_up, "Up")
screen.onkeypress(r_paddle.go_down, "Down")

# --- Основной Игровой Цикл ---
game_is_on = True
while game_is_on:
    time.sleep(0.001) # Очень маленькая задержка для контроля скорости
    screen.update()
    ball.move()

    # 1. Отскок от верхней/нижней стенки
    if ball.ycor() > HEIGHT/2 - 10 or ball.ycor() < -HEIGHT/2 + 10:
        ball.bounce_y()

    # 2. Отскок от ракеток
    # От правой ракетки
    if ball.distance(r_paddle) < 50 and ball.xcor() > WIDTH/2 - 70:
        ball.setx(WIDTH/2 - 70) # Предотвращаем застревание
        ball.bounce_x()

    # От левой ракетки
    if ball.distance(l_paddle) < 50 and ball.xcor() < -WIDTH/2 + 70:
        ball.setx(-WIDTH/2 + 70) # Предотвращаем застревание
        ball.bounce_x()

    # 3. Пропуск мяча (Гол)
    # Правый игрок пропустил (очко левому)
    if ball.xcor() > WIDTH/2:
        ball.reset_position()
        scoreboard.l_point()
        time.sleep(0.5) # Пауза после гола

    # Левый игрок пропустил (очко правому)
    if ball.xcor() < -WIDTH/2:
        ball.reset_position()
        scoreboard.r_point()
        time.sleep(0.5) # Пауза после гола

screen.mainloop()