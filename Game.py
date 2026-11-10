
import tkinter as tk
import random


# ==============================
# CLASS GAME OBJECT
# ==============================
class GameObject:
    def __init__(self, canvas, item):
        self.canvas = canvas
        self.item = item

    def get_position(self):
        return self.canvas.coords(self.item)

    def move(self, x, y):
        self.canvas.move(self.item, x, y)

    def delete(self):
        self.canvas.delete(self.item)


# ==============================
# CLASS BALL
# ==============================
class Ball(GameObject):
    def __init__(self, canvas, x, y, speed=6):
        self.radius = 10
        self.direction = [random.choice([-1, 1]), -1]
        self.speed = speed

        item = canvas.create_oval(
            x - self.radius, y - self.radius,
            x + self.radius, y + self.radius,
            fill="white", outline="#3498db", width=2
        )

        super().__init__(canvas, item)

    def update(self):
        coords = self.get_position()
        width = self.canvas.winfo_width()

        # Pantulan dinding kiri dan kanan
        if coords[0] <= 0 and self.direction[0] < 0:
            self.direction[0] *= -1

        elif coords[2] >= width and self.direction[0] > 0:
            self.direction[0] *= -1

        # Pantulan dinding atas
        if coords[1] <= 0 and self.direction[1] < 0:
            self.direction[1] *= -1

        self.move(
            self.direction[0] * self.speed,
            self.direction[1] * self.speed
        )


# ==============================
# CLASS PADDLE
# ==============================
class Paddle(GameObject):
    def __init__(self, canvas, x, y):
        self.width = 100
        self.height = 12

        item = canvas.create_rectangle(
            x - self.width / 2,
            y - self.height / 2,
            x + self.width / 2,
            y + self.height / 2,
            fill="#f1c40f",
            outline="white",
            width=2
        )

        super().__init__(canvas, item)

    def move_paddle(self, offset):
        coords = self.get_position()
        width = self.canvas.winfo_width()

        if coords[0] + offset >= 0 and coords[2] + offset <= width:
            self.move(offset, 0)


# ==============================
# CLASS BRICK
# ==============================
class Brick(GameObject):

    COLORS = {
        1: "#2ecc71",
        2: "#3498db",
        3: "#e74c3c"
    }

    def __init__(self, canvas, x, y, hits):
        self.width = 75
        self.height = 20
        self.hits = hits

        item = canvas.create_rectangle(
            x - self.width / 2,
            y - self.height / 2,
            x + self.width / 2,
            y + self.height / 2,
            fill=self.COLORS[hits],
            outline="white",
            width=2,
            tags="brick"
        )

        super().__init__(canvas, item)

    def hit(self):
        self.hits -= 1

        if self.hits <= 0:
            self.delete()
            return True

        self.canvas.itemconfig(
            self.item,
            fill=self.COLORS[self.hits]
        )
        return False


