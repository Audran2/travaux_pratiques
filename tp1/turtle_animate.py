import turtle
import random
from shaky_window import shake_window

def animate_entry(t, x, y):
    turtle.tracer(0)
    t.penup()
    t.speed(10)

    # 🔄 0) Rotation d'intro
    for _ in range(12):
        t.right(30)
        turtle.update()

    # 1) Arrivée glissée
    t.goto(x - 300, y)
    for i in range(30):
        t.goto(x - 300 + i * 10, y)
        turtle.update()

    # 2) Petit saut cartoon
    for h in [10, 20, 30, 20, 10, 0]:
        t.goto(x, y + h)
        turtle.update()

    # 3) Tremblement comique (gardé)
    for _ in range(6):
        t.goto(x + random.randint(-5, 5), y + random.randint(-5, 5))
        turtle.update()

    # 4) Secouer la fenêtre (fun)
    shake_window(turtle.Screen(), intensity=25, duration=0.3)

    # 🔄 5) Rotation finale
    t.goto(x, y)
    t.pendown()
    for _ in range(12):
        t.left(30)
        turtle.update()

    t.penup()
    t.goto(x, y)
    t.setheading(0)
    t.pendown()

    turtle.tracer(1)