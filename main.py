import tkinter as tk
from tkinter import messagebox, CENTER, PhotoImage
import time
import random
from PIL import Image, ImageTk

LARGE_FONT = ("Verdana", 12)
app_running = True

size_x = 300
size_y = 300
x = 10
y = 10
step_x = size_x // x
step_y = size_y // y

computer_ships_list = []

move = False
computer_vs_human = True
random_points = True
hits = [[-1 for _ in range(x + 1)] for _ in range(y + 1)]
user_hits = [[-1 for _ in range(x + 1)] for _ in range(y + 1)]
shots = [[0 for _ in range(x + 1)] for _ in range(y + 1)]
user_shots = [[0 for _ in range(x + 1)] for _ in range(y + 1)]
ships = {'carrier': 5, 'battleship': 4, 'cruiser': 3, 'submarine': 3, 'destroyer': 2}
number_of_ships = 5
computer_ships = [[0 for _ in range(x + 1)] for _ in range(y + 1)]
user_ships = [[0 for _ in range(x + 1)] for _ in range(y + 1)]

if computer_vs_human:
    add_to_label = " (Komputer)"
    move = False
else:
    add_to_label = ""
    move = False


def close():
    global app_running, app
    if messagebox.askokcancel("Wyjście", "Czy na pewno chcesz zakończyć grę?"):
        app_running = False
        app.destroy()


def print_field(xx, yy, canvas):
    alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    for i in range(0, x + 1):
        canvas.create_line(size_x // x * i + xx, 0 + yy, size_x // x * i + xx, size_y + yy)
    for i in range(0, y + 1):
        canvas.create_line(0 + xx, size_y // y * i + yy, size_y + xx, size_y // y * i + yy)
    for i in range(0, x):
        canvas.create_text(xx + 30 // 2 + step_x * i, step_y // 2, text=alphabet[i], font="Monaco", fill="red")
    for i in range(0, x):
        canvas.create_text(xx - step_x // 2, step_y * i + yy + step_y // 2, text=i + 1, font="Monaco", fill="red")


class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.protocol("WM_DELETE_WINDOW", close)
        self.resizable(0, 0)
        self.title("Battleship")
        self.wm_attributes("-topmost", 1)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        canvas = tk.Canvas(self, width=size_x + 180 + size_x + 30, height=size_y + 200, bd=0, highlightthickness=0)
        canvas.pack()
        label = tk.Label(canvas, text="Statki", font=("Monaco", 30))
        label.place(x=300, y=50)

        rb_var = tk.BooleanVar()
        rb1 = tk.Radiobutton(canvas, text="Człowiek vs Komputer", variable=rb_var, value=1,
                             command=lambda: change_rb(rb_var))
        rb2 = tk.Radiobutton(canvas, text="Człowiek vs Człowiek", variable=rb_var, value=0,
                             command=lambda: change_rb(rb_var))

        canvas.create_text(150, 230, text="Options:", font=("Monaco", 10))
        rb1.place(x=120, y=250)
        rb2.place(x=120, y=280)
        if computer_vs_human:
            rb1.select()

        for i in range(0, 5):
            canvas.create_rectangle(500 + i * step_x, 150, 500 + i * step_x + step_x, 150 + step_x, fill='#F5DA81')
        canvas.create_text(500 + 6 * step_x + step_x // 2, 150 + step_y // 2, text=" » Carrier", font=("Monaco", 10))
        for i in range(0, 4):
            canvas.create_rectangle(500 + i * step_x, 200, 500 + i * step_x + step_x, 200 + step_x, fill='#81F781')
        canvas.create_text(500 + 6 * step_x + step_x, 200 + step_y // 2, text=" » Battleship", font=("Monaco", 10))
        for i in range(0, 3):
            canvas.create_rectangle(500 + i * step_x, 250, 500 + i * step_x + step_x, 250 + step_x, fill='#5882FA')
        canvas.create_text(500 + 6 * step_x + step_x // 2, 250 + step_y // 2, text=" » Cruiser", font=("Monaco", 10))
        for i in range(0, 3):
            canvas.create_rectangle(500 + i * step_x, 300, 500 + i * step_x + step_x, 300 + step_x, fill='#FA58AC')
        canvas.create_text(500 + 6 * step_x + step_x // 2, 300 + step_y // 2, text=" » Submarine", font=("Monaco", 10))
        for i in range(0, 2):
            canvas.create_rectangle(500 + i * step_x, 350, 500 + i * step_x + step_x, 350 + step_x, fill='#848484')
        canvas.create_text(500 + 6 * step_x + step_x // 2, 350 + step_y // 2, text=" » Destroyer", font=("Monaco", 10))

        self.our_button = PhotoImage(file="button_start.png")
        self.our_button = self.our_button.subsample(1, 1)
        # self.id_img1 = canvas.create_image(200, 300, anchor="nw", image=self.our_button)

        button = tk.Button(self, image=self.our_button, highlightthickness=0, bd=0,
                           command=lambda: controller.show_frame(PageOne))
        button.place(x=120, y=150)


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        global computer_ships, user_ships
        changing_page()
        tk.Frame.__init__(self, parent)

        canvas = tk.Canvas(self, width=size_x + 180 + size_x + 30, height=size_y + 200, bd=0, highlightthickness=0)
        canvas.pack()
        canvas.create_rectangle(30, 30, size_x + 30, size_y + 30, fill="white")
        canvas.create_rectangle(size_x + 180, 30, size_x + 180 + size_x, size_y + 30, fill="white")

        canvas.bind_all("<Button-1>", lambda event: add_to_all(event, canvas))
        canvas.bind_all("<Button-3>", lambda event: add_to_all(event, canvas))

        print_field(30, 30, canvas)
        print_field(size_x + 180, 30, canvas)

        self.our_button = PhotoImage(file="button_menu.png")
        self.our_button = self.our_button.subsample(1, 1)

        b1 = tk.Button(canvas, text="<-Pokaż statki", font=("Monaco", 8), command=lambda: show_computer_ships(canvas))
        b1.place(x=30, y=370)
        b2 = tk.Button(canvas, text="Pokaż statki->", font=("Monaco", 8), command=lambda: show_user_ships(canvas))
        b2.place(x=30, y=400)

        self.button = PhotoImage(file="button_nowa-gra.png")
        self.button = self.button.subsample(1, 1)
        b3 = tk.Button(canvas, text="Nowa gra ", image=self.button, highlightthickness=0, bd=0, font=("Monaco", 8),
                       command=lambda: start_new_game(canvas))
        b3.place(x=30, y=440)



        computer_ships = generate_ships()
        user_ships = generate_ships()

        current_move(move, canvas)

        button1 = tk.Button(self, image=self.our_button, highlightthickness=0, bd=0,
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

    def current_computer_move(self, move, canvas):
        pass


def change_rb(rb_var):
    global computer_vs_human, add_to_label
    print(rb_var.get())
    if rb_var.get():
        computer_vs_human = True
        add_to_label = " (Komputer)"
    else:
        computer_vs_human = False
        add_to_label = " "


def show_user_ships(canvas):
    global computer_ships_list
    for i in range(0, x):
        for j in range(0, y):
            if user_ships[j][i] > 0:
                _id = canvas.create_rectangle(size_x + 150 + i * step_x + step_x, j * step_y + step_y,
                                              size_x + 150 + i * step_x + step_x + step_x, j * step_y + step_y + step_y,
                                              fill="pink")
                computer_ships_list.append(_id)


def show_computer_ships(canvas):
    global computer_ships_list
    for i in range(0, x):
        for j in range(0, y):
            if computer_ships[j][i] > 0:
                _id = canvas.create_rectangle(i * step_x + step_x, j * step_y + step_y, i * step_x + step_x + step_x,
                                              j * step_y + step_y + step_y, fill="pink")
                computer_ships_list.append(_id)


def start_new_game(canvas):
    global computer_ships_list, hits, shots, computer_ships, user_ships, user_hits, user_shots, move
    if messagebox.askokcancel("Nowa gra", "Czy na pewno chcesz rozpocząć nową grę?"):
        for i in computer_ships_list:
            canvas.delete(i)
        computer_ships_list = []
        computer_ships = generate_ships()
        user_ships = generate_ships()
        hits = [[-1 for _ in range(x + 1)] for _ in range(y + 1)]
        shots = [[0 for _ in range(x + 1)] for _ in range(y + 1)]
        user_hits = [[-1 for _ in range(x + 1)] for _ in range(y + 1)]
        user_shots = [[0 for _ in range(x + 1)] for _ in range(y + 1)]
        move = False


def changing_page():
    global computer_ships_list, hits, shots, computer_ships, user_ships, user_hits, user_shots, move
    computer_ships_list = []
    computer_ships = generate_ships()
    user_ships = generate_ships()
    hits = [[-1 for _ in range(x + 1)] for _ in range(y + 1)]
    shots = [[0 for _ in range(x + 1)] for _ in range(y + 1)]
    user_hits = [[-1 for _ in range(x + 1)] for _ in range(y + 1)]
    user_shots = [[0 for _ in range(x + 1)] for _ in range(y + 1)]
    move = False


def draw_point(x_point, y_point, xx, yy, list_of_ships, canvas):
    if list_of_ships[y_point - yy][x_point - xx] == 1:
        fill = canvas.create_rectangle(x_point * step_x, y_point * step_y, x_point * step_x + step_x,
                                       y_point * step_y + step_y, fill="#D82727")
        computer_ships_list.append(fill)
    else:
        fill = canvas.create_rectangle(x_point * step_x, y_point * step_y, x_point * step_x + step_x,
                                       y_point * step_y + step_y, fill="#6495ED")
        computer_ships_list.append(fill)


def check_winner1(x_point, y_point):
    victory = False
    if computer_ships[y_point][x_point] > 0:
        shots[y_point][x_point] = 1
    sum_computer_ships = sum(sum(i) for i in zip(*computer_ships))
    sum_shots = sum(sum(i) for i in zip(*shots))
    if sum_computer_ships == sum_shots:
        victory = True
    return victory


def check_winner2(x_point, y_point):
    victory = False
    if user_ships[y_point][x_point] > 0:
        user_shots[y_point][x_point] = 1
    sum_user_ships = sum(sum(i) for i in zip(*user_ships))
    sum_user_shots = sum(sum(i) for i in zip(*user_shots))
    if sum_user_ships == sum_user_shots:
        victory = True
    return victory


def computer_move(canvas):
    global move, computer_ships_list, hits, user_hits
    move = False
    ip_x = random.randint(0, x - 1)
    ip_y = random.randint(0, y - 1)
    while not hits[ip_y][ip_x] == -1:
        ip_x = random.randint(0, x - 1)
        ip_y = random.randint(0, y - 1)
    hits[ip_y][ip_x] = 0
    print(ip_x, ip_y)
    canvas.update()
    time.sleep(1)
    draw_point(ip_x + 1, ip_y + 1, 0, 0, user_ships, canvas)
    if check_winner1(ip_x - 1, ip_y - 1):
        move = True
        text = "Komputer wygrał!"
        user_hits = [[1 for _ in range(x + 1)] for _ in range(y + 1)]
        hits = [[1 for _ in range(x + 1)] for _ in range(y + 1)]
        id1 = canvas.create_rectangle(step_x * 8, step_y * 6 + step_y // 2,
                                      size_x + 180 + step_x * 3,
                                      step_y * 9, fill="#F79F81")
        computer_ships_list.append(id1)
        id2 = canvas.create_rectangle(step_x * 8 + step_x // 2, step_y * 7,
                                      size_x + 180 + step_x * 2 + step_x // 2,
                                      step_y * 8 + step_y // 2, fill="#F3F781")
        computer_ships_list.append(id2)
        id3 = canvas.create_text(step_x * 13 + step_x // 2, step_y * 8, text=text, font=("Monaco", 25),
                                 justify=CENTER)
        computer_ships_list.append(id3)
    current_move(move, canvas)


def add_to_all(event, canvas):
    global hits, user_hits, user_ships, computer_ships, move
    _type = 0
    if event.num == 3:
        _type = 1
    mouse_x = canvas.winfo_pointerx() - canvas.winfo_rootx()
    mouse_y = canvas.winfo_pointery() - canvas.winfo_rooty()
    ip_x = mouse_x // step_x
    ip_y = mouse_y // step_y
    if x >= ip_x > 0 and y >= ip_y > 0 and move:
        if hits[ip_y - 1][ip_x - 1] == -1:
            draw_point(ip_x, ip_y, 1, 1, computer_ships, canvas)
            hits[ip_y - 1][ip_x - 1] = 0
            move = False
            if check_winner1(ip_x - 1, ip_y - 1):
                move = True
                text = "Gracz 2 wygrał!"
                user_hits = [[1 for _ in range(x + 1)] for _ in range(y + 1)]
                hits = [[1 for _ in range(x + 1)] for _ in range(y + 1)]
                id1 = canvas.create_rectangle(step_x * 8, step_y * 6 + step_y // 2,
                                              size_x + 180 + step_x * 3,
                                              step_y * 9, fill="#F79F81")
                computer_ships_list.append(id1)
                id2 = canvas.create_rectangle(step_x * 8 + step_x // 2, step_y * 7,
                                              size_x + 180 + step_x * 2 + step_x // 2,
                                              step_y * 8 + step_y // 2, fill="#F3F781")
                computer_ships_list.append(id2)
                id3 = canvas.create_text(step_x * 13 + step_x // 2, step_y * 8, text=text, font=("Monaco", 25),
                                         justify=CENTER)
                computer_ships_list.append(id3)

    if 25 >= ip_x > 15 and y >= ip_y > 0 and not move:
        if user_hits[ip_y - 1][ip_x - 16] == -1:
            draw_point(ip_x, ip_y, 16, 1, user_ships, canvas)
            user_hits[ip_y - 1][ip_x - 16] = 0
            move = True
            if check_winner2(ip_x - 16, ip_y - 1):
                move = False
                text = "Gracz 1 wygrał!"
                user_hits = [[1 for _ in range(x + 1)] for _ in range(y + 1)]
                hits = [[1 for _ in range(x + 1)] for _ in range(y + 1)]
                id1 = canvas.create_rectangle(step_x * 8, step_y * 6 + step_y // 2,
                                              size_x + 180 + step_x * 3,
                                              step_y * 9, fill="#F79F81")
                computer_ships_list.append(id1)
                id2 = canvas.create_rectangle(step_x * 8 + step_x // 2, step_y * 7,
                                              size_x + 180 + step_x * 2 + step_x // 2,
                                              step_y * 8 + step_y // 2, fill="#F3F781")
                computer_ships_list.append(id2)
                id3 = canvas.create_text(step_x * 13 + step_x // 2, step_y * 8, text=text, font=("Monaco", 25),
                                         justify=CENTER)
                computer_ships_list.append(id3)
            elif computer_vs_human:
                current_move(move, canvas)
                computer_move(canvas)
    current_move(move, canvas)


def generate_ships():  # generation of computer ships
    ships_list = [5, 4, 3, 3, 2]
    sum_all_ships = sum(ships_list)
    sum_of_ships = 0
    success = 0
    while sum_of_ships != sum_all_ships:
        enemy_ships = [[0 for _ in range(x + 1)] for _ in range(y + 1)]

        for i in range(0, number_of_ships):
            length_of_ship = ships_list[i]
            direction = random.randrange(1, 3)  # 1 - h, 2 - v

            if direction == 1:
                x_coord = random.randrange(0, x)
                if x_coord + length_of_ship > x:
                    x_coord = x_coord - length_of_ship

                y_coord = random.randrange(0, y)

                for j in range(0, length_of_ship):
                    try:
                        check_near_ships = enemy_ships[y_coord][x_coord - 1] + \
                                           enemy_ships[y_coord][x_coord + j] + \
                                           enemy_ships[y_coord][x_coord + j + 1] + \
                                           enemy_ships[y_coord - 1][x_coord - 1] + \
                                           enemy_ships[y_coord + 1][x_coord + j + 1] + \
                                           enemy_ships[y_coord - 1][x_coord + j + 1] + \
                                           enemy_ships[y_coord + 1][x_coord + j] + \
                                           enemy_ships[y_coord - 1][x_coord + j]
                        if check_near_ships == 0:
                            success = 1
                        else:
                            success = 0
                            i = i - 1
                            break
                    except Exception:
                        pass

                if success == 1:
                    for j in range(0, length_of_ship):
                        enemy_ships[y_coord][x_coord + j] = 1

            if direction == 2:
                y_coord = random.randrange(0, y)
                if y_coord + length_of_ship > y:
                    y_coord = y_coord - length_of_ship

                x_coord = random.randrange(0, x)

                for j in range(0, length_of_ship):
                    try:
                        check_near_ships = enemy_ships[y_coord - 1][x_coord] + \
                                           enemy_ships[y_coord + j][x_coord] + \
                                           enemy_ships[y_coord + j + 1][x_coord] + \
                                           enemy_ships[y_coord + j + 1][x_coord + 1] + \
                                           enemy_ships[y_coord + j + 1][x_coord - 1] + \
                                           enemy_ships[y_coord + j][x_coord + 1] + \
                                           enemy_ships[y_coord + j][x_coord - 1] + \
                                           enemy_ships[y_coord][x_coord]
                        if check_near_ships == 0:
                            success = 1
                        else:
                            success = 0
                            i = i - 1
                            break
                    except Exception:
                        pass

                if success == 1:
                    for j in range(0, length_of_ship):
                        enemy_ships[y_coord + j][x_coord] = 1

        sum_of_ships = 0
        for i in range(0, x):
            for j in range(0, y):
                if enemy_ships[j][i] > 0:
                    sum_of_ships = sum_of_ships + 1

    return enemy_ships


def current_move(user_move, canvas):
    global add_to_label
    canvas.update()
    t1 = tk.Label(canvas, text="Gracz #1", font=("Monaco", 14))
    t1.place(x=30, y=size_x + 40)
    t2 = tk.Label(canvas, font=("Monaco", 14))
    t2.configure(text="Gracz #2")
    t2.place(x=size_x + 180, y=size_x + 40)
    t3 = tk.Label(canvas, font=("Monaco", 10))
    t3.configure(bg="#BE81F7")
    t3.place(x=25 + size_x + 20, y=0)
    t4 = tk.Label(canvas, font=("Monaco", 30))
    t4.place(x=size_x + 60, y=70)

    if user_move:
        t1.configure(bg="#D82727")
        t2.configure(bg="#f0f0f0")
        t3.configure(text="Tura gracza 2")
        t4.configure(text=" » ")
    else:
        t2.configure(bg="#D82727")
        t1.configure(bg="#f0f0f0")
        t3.configure(text="Tura gracza 1")
        t4.configure(text=" « ")


app = SeaofBTCapp()
app.mainloop()
