
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


# ==============================
# CLASS GAME
# ==============================
class Game(tk.Frame):

    def __init__(self, master):
        super().__init__(master)

        self.master = master
        self.width = 610
        self.height = 450

        self.score = 0
        self.lives = 3
        self.level = 1

        self.running = False
        self.game_over = False
        self.after_id = None

        self.items = {}
        self.ball = None

        self.pack()

        # Canvas permainan
        self.canvas = tk.Canvas(
            self,
            width=self.width,
            height=self.height,
            bg="#172554",
            highlightthickness=0
        )
        self.canvas.pack()

        # Informasi skor
        self.hud = self.canvas.create_text(
            100, 20,
            text="Score: 0",
            fill="white",
            font=("Arial", 14, "bold")
        )

        self.life_text = self.canvas.create_text(
            300, 20,
            text="Lives: 3",
            fill="white",
            font=("Arial", 14, "bold")
        )

        self.level_text = self.canvas.create_text(
            500, 20,
            text="Level: 1",
            fill="white",
            font=("Arial", 14, "bold")
        )

        # Membuat paddle
        self.paddle = Paddle(
            self.canvas,
            self.width / 2,
            410
        )

        self.items[self.paddle.item] = self.paddle

        # Membuat bola dan balok
        self.create_bricks()
        self.add_ball()

        # Tampilan menu awal
        self.show_message(
            "BREAKOUT GAME",
            "Tekan tombol START untuk bermain"
        )

        # Tombol kontrol
        button_frame = tk.Frame(self)
        button_frame.pack(pady=8)

        self.start_button = tk.Button(
            button_frame,
            text="START",
            width=12,
            bg="#27ae60",
            fg="white",
            command=self.start_game
        )
        self.start_button.pack(side="left", padx=5)

        self.pause_button = tk.Button(
            button_frame,
            text="PAUSE",
            width=12,
            bg="#f39c12",
            fg="white",
            command=self.pause_game
        )
        self.pause_button.pack(side="left", padx=5)

        self.restart_button = tk.Button(
            button_frame,
            text="RESTART",
            width=12,
            bg="#e74c3c",
            fg="white",
            command=self.restart_game
        )
        self.restart_button.pack(side="left", padx=5)

        # Keyboard
        self.master.bind("<Left>", self.move_left)
        self.master.bind("<Right>", self.move_right)
        self.master.bind("<space>", self.space_control)

    # ==============================
    # MEMBUAT BALOK
    # ==============================
    def create_bricks(self):
        for row in range(4):
            for col in range(7):

                x = 75 + col * 77
                y = 70 + row * 28

                hits = random.randint(1, 3)

                brick = Brick(
                    self.canvas,
                    x,
                    y,
                    hits
                )

                self.items[brick.item] = brick

    # ==============================
    # MEMBUAT BOLA
    # ==============================
    def add_ball(self):
        if self.ball is not None:
            self.ball.delete()

        paddle_coords = self.paddle.get_position()

        x = (paddle_coords[0] + paddle_coords[2]) / 2

        self.ball = Ball(
            self.canvas,
            x,
            390,
            speed=5 + self.level
        )

    # ==============================
    # MENAMPILKAN PESAN
    # ==============================
    def show_message(self, title, subtitle):
        self.canvas.delete("message")

        self.canvas.create_text(
            self.width / 2,
            200,
            text=title,
            fill="#f1c40f",
            font=("Arial", 28, "bold"),
            tags="message"
        )

        self.canvas.create_text(
            self.width / 2,
            245,
            text=subtitle,
            fill="white",
            font=("Arial", 13),
            tags="message"
        )

    # ==============================
    # UPDATE SCORE DAN HUD
    # ==============================
    def update_hud(self):
        self.canvas.itemconfig(
            self.hud,
            text=f"Score: {self.score}"
        )

        self.canvas.itemconfig(
            self.life_text,
            text=f"Lives: {self.lives}"
        )

        self.canvas.itemconfig(
            self.level_text,
            text=f"Level: {self.level}"
        )

    # ==============================
    # GERAK PADDLE
    # ==============================
    def move_left(self, event=None):
        self.paddle.move_paddle(-25)

    def move_right(self, event=None):
        self.paddle.move_paddle(25)

    # ==============================
    # MEMULAI GAME
    # ==============================
    def start_game(self):
        if self.game_over:
            return

        if self.running:
            return

        self.running = True
        self.canvas.delete("message")

        self.start_button.config(state="disabled")

        self.game_loop()

    # ==============================
    # PAUSE GAME
    # ==============================
    def pause_game(self):
        if self.game_over:
            return

        if self.running:
            self.running = False

            if self.after_id is not None:
                self.after_cancel(self.after_id)
                self.after_id = None

            self.show_message(
                "GAME PAUSED",
                "Tekan SPACE atau START untuk melanjutkan"
            )

            self.start_button.config(state="normal")

        else:
            self.start_game()

    def space_control(self, event=None):
        self.pause_game()

    # ==============================
    # CEK TABRAKAN
    # ==============================
    def check_collisions(self):

        ball_coords = self.ball.get_position()

        items = self.canvas.find_overlapping(
            *ball_coords
        )

        objects = [
            self.items[item]
            for item in items
            if item in self.items
        ]

        for obj in objects:

            # Tabrakan dengan paddle
            if obj == self.paddle:

                if self.ball.direction[1] > 0:
                    ball_center = (
                        ball_coords[0] + ball_coords[2]
                    ) / 2

                    paddle_coords = self.paddle.get_position()

                    paddle_center = (
                        paddle_coords[0] + paddle_coords[2]
                    ) / 2

                    difference = (
                        ball_center - paddle_center
                    ) / (self.paddle.width / 2)

                    self.ball.direction[0] = max(
                        -1,
                        min(1, difference)
                    )

                    if abs(self.ball.direction[0]) < 0.2:
                        self.ball.direction[0] = random.choice(
                            [-0.3, 0.3]
                        )

                    self.ball.direction[1] = -1

            # Tabrakan dengan brick
            elif isinstance(obj, Brick):

                self.ball.direction[1] *= -1

                destroyed = obj.hit()

                self.score += 10

                if destroyed:
                    self.items.pop(obj.item, None)

                self.update_hud()

                # Satu balok diproses setiap frame
                break

    # ==============================
    # LEVEL BERIKUTNYA
    # ==============================
    def next_level(self):

        self.running = False

        if self.level >= 3:
            self.win_game()
            return

        self.level += 1

        self.create_bricks()
        self.add_ball()
        self.update_hud()

        self.show_message(
            f"LEVEL {self.level}",
            "Tekan START untuk melanjutkan"
        )

        self.start_button.config(state="normal")

    # ==============================
    # KEHILANGAN NYAWA
    # ==============================
    def lose_life(self):

        self.lives -= 1
        self.update_hud()

        if self.lives <= 0:
            self.end_game()
            return

        self.running = False

        self.add_ball()

        self.show_message(
            "BALL LOST!",
            "Tekan START untuk mencoba lagi"
        )

        self.start_button.config(state="normal")

    # ==============================
    # MENANG
    # ==============================
    def win_game(self):

        self.running = False
        self.game_over = True

        self.show_message(
            "YOU WIN!",
            f"Skor akhir: {self.score}"
        )

        self.start_button.config(state="disabled")

    # ==============================
    # GAME OVER
    # ==============================
    def end_game(self):

        self.running = False
        self.game_over = True

        self.show_message(
            "GAME OVER!",
            f"Skor akhir: {self.score}"
        )

        self.start_button.config(state="disabled")

    # ==============================
    # RESTART GAME
    # ==============================
    def restart_game(self):

        if self.after_id is not None:
            self.after_cancel(self.after_id)
            self.after_id = None

        self.running = False
        self.game_over = False

        self.score = 0
        self.lives = 3
        self.level = 1

        self.canvas.delete("all")

        self.items.clear()

        # Membuat ulang HUD
        self.hud = self.canvas.create_text(
            100, 20,
            text="Score: 0",
            fill="white",
            font=("Arial", 14, "bold")
        )

        self.life_text = self.canvas.create_text(
            300, 20,
            text="Lives: 3",
            fill="white",
            font=("Arial", 14, "bold")
        )

        self.level_text = self.canvas.create_text(
            500, 20,
            text="Level: 1",
            fill="white",
            font=("Arial", 14, "bold")
        )

        self.paddle = Paddle(
            self.canvas,
            self.width / 2,
            410
        )

        self.items[self.paddle.item] = self.paddle

        self.create_bricks()
        self.add_ball()
        self.update_hud()

        self.show_message(
            "BREAKOUT GAME",
            "Tekan tombol START untuk bermain"
        )

        self.start_button.config(state="normal")

    # ==============================
    # GAME LOOP
    # ==============================
    def game_loop(self):

        if not self.running:
            return

        self.ball.update()

        self.check_collisions()

        # Cek apakah semua balok habis
        num_bricks = len(
            self.canvas.find_withtag("brick")
        )

        if num_bricks == 0:
            self.next_level()
            return

        # Cek apakah bola jatuh
        if self.ball.get_position()[3] >= self.height:
            self.lose_life()
            return

        # Mengulang permainan setiap 20 ms
        self.after_id = self.after(
            20,
            self.game_loop
        )


# ==============================
# MENJALANKAN APLIKASI
# ==============================
if __name__ == "__main__":

    root = tk.Tk()

    root.title("Breakout Game - Python Tkinter")
    root.resizable(False, False)
    root.configure(bg="#172554")

    game = Game(root)

    root.mainloop()
