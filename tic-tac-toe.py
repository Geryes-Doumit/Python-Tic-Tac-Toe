import tkinter as tk
import numpy as np
import pyglet

turn_to_player = {1: "X", -1: "O"}
size = 500
BgColor = "beige"
LineColor = "#662901"
WinColor = "red"
pyglet.font.add_directory('fonts')
font = "Wearedimdam"
font2 = "BLOXAT"
BoxSize = size // 3


class MouseAndBoard:
    ButtonPress = False
    MouseCoords = 0, 0

    def __init__(self):
        self.matrix = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        self.Index = 0, 0

    def left_click(self, event):
        if str(event.widget) == ".!canvas":
            self.MouseCoords = event.x, event.y
            self.ButtonPress = True

    def input_on_board(self):
        if self.MouseCoords[0] < size and self.MouseCoords[1] < size:
            self.Index = self.MouseCoords[1] // (size // 3), self.MouseCoords[0] // (size // 3)
            if self.matrix[self.Index] == 0:
                self.matrix[self.Index] = game.turn
            else:
                label.configure(text="Already taken!", font=(font2, size // 29))
                self.ButtonPress = False

    def restart(self):
        self.matrix = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        game.turn = 1
        game.NbreTours = 0
        canvas.delete("all")
        self.ButtonPress = False
        game.WIN = False
        game.DRAW = False
        line1 = canvas.create_line(size // 3, 0, size // 3, size, width=3, fill=LineColor)
        line2 = canvas.create_line(2 * size // 3, 0, 2 * size // 3, size, width=3, fill=LineColor)
        line3 = canvas.create_line(0, size // 3, size, size // 3, width=3, fill=LineColor)
        line4 = canvas.create_line(0, 2 * size // 3, size, 2 * size // 3, width=3, fill=LineColor)
        canvas.pack()
        label.configure(text="Player " + turn_to_player[game.turn] + "'s turn", font=(font2, size // 29))


class Jeton:
    def __init__(self, color, x, y):
        self.x = x
        self.y = y
        self.color = color
        self.CanvasPrint = canvas.create_text(x, y, fill=color, font=(font, str(size // 8)),
                                              text=turn_to_player[game.turn])


class Game:
    WIN = False
    DRAW = False
    gameover = False
    turn = 1
    NbreTours = 0
    WinIndex = [(0, 0), (0, 0), (0, 0)]

    def win_or_draw(self):
        for i in range(len(Board.matrix)):
            if Board.matrix[i][0] == Board.matrix[i][1] == Board.matrix[i][2] != 0:
                self.WIN = True
                self.WinIndex = [(i, 0), (i, 1), (i, 2)]
            elif Board.matrix[0][i] == Board.matrix[1][i] == Board.matrix[2][i] != 0:
                self.WIN = True
                self.WinIndex = [(0, i), (1, i), (2, i)]
        if Board.matrix[0][0] == Board.matrix[1][1] == Board.matrix[2][2] != 0:
            self.WIN = True
            self.WinIndex = [(0, 0), (1, 1), (2, 2)]
        elif Board.matrix[0][2] == Board.matrix[1][1] == Board.matrix[2][0] != 0:
            self.WIN = True
            self.WinIndex = [(0, 2), (1, 1), (2, 0)]

        if self.NbreTours == 9 and not self.WIN:
            self.DRAW = True

    def playing(self):
        if not self.WIN and not self.DRAW:
            self.gameover = False
            if Board.ButtonPress:
                Board.input_on_board()
                if Board.ButtonPress:
                    x = (Board.Index[1] * BoxSize + BoxSize // 2)
                    y = (Board.Index[0] * BoxSize + BoxSize // 2)
                    text = Jeton(LineColor, x, y)
                    canvas.pack()
                    self.turn = -self.turn
                    self.NbreTours += 1
                    self.win_or_draw()
                Board.ButtonPress = False
                label.configure(text="Player " + turn_to_player[self.turn] + "'s turn", font=(font2, size // 29))
        if self.WIN and not self.gameover:
            self.turn *= -1
            for i in range(3):
                lign, column = self.WinIndex[i]
                text = Jeton(WinColor, (column * BoxSize + BoxSize // 2), (lign * BoxSize + BoxSize // 2))
                canvas.pack()
            label.configure(text="Player " + turn_to_player[self.turn] + " wins!", font=(font2, size // 29))
            self.gameover = True

        elif self.DRAW and not self.gameover:
            label.configure(text="Draw, better luck next time!", font=(font2, size // 29))
            self.gameover = True

        window.after(10, self.playing)


Board = MouseAndBoard()
game = Game()

window = tk.Tk()
window.title("Game time!")
canvas = tk.Canvas(window, bg=BgColor, width=size, height=size)
line1 = canvas.create_line(size // 3, 0, size // 3, size, width=3, fill=LineColor)
line2 = canvas.create_line(2 * size // 3, 0, 2 * size // 3, size, width=3, fill=LineColor)
line3 = canvas.create_line(0, size // 3, size, size // 3, width=3, fill=LineColor)
line4 = canvas.create_line(0, 2 * size // 3, size, 2 * size // 3, width=3, fill=LineColor)
canvas.pack()
label = tk.Label(text="Player " + turn_to_player[game.turn] + "'s turn", font=(font2, size // 29))
label.pack()
button1 = tk.Button(window, text='Quit Game', command=window.destroy, width=12)
button2 = tk.Button(window, text='New Game', command=Board.restart, width=12)
button2.pack(side="left", padx=(size // 6), pady=10)
button1.pack(side="right", padx=(size // 6), pady=10)

window.bind("<Button 1>", Board.left_click)
game.playing()
window.mainloop()
