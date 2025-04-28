from turtle import *
screen = Screen()
screen.bgcolor("black")
pencolor("red")
speed(0)
for i in range(180):
    circle(190-i,90)
    lt(60)
    circle(190-i,90)
    lt(18)

mainloop()
