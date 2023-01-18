import game as game
import tkinter as tk
from tkinter import PhotoImage, ttk, messagebox


class GraphicalInterfaces():
    def __init__(self):
        self.grid = game.createGame(12, 10, 2, False)
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=self.grid.getWidth() *
                                40, height=self.grid.getHeight()*40)
        self.agreement = tk.StringVar()
        self.rectangles = []
        self.image_container = []
        self.casePNG = [PhotoImage(file="image/noHole.png"),
                        PhotoImage(file="image/singleHole.png"),
                        PhotoImage(file="image/twoHoles.png"),
                        PhotoImage(file="image/threeHoles.png")]

        self.root.geometry('1500x750')
        self.root.title('Expansion')
        self.canvas.pack()
        self.initializeCanvas()

        self.spinbox1 = self.createSpinbox(True,
                                           "Enter the height of the board :", 3, 10)
        self.spinbox2 = self.createSpinbox(True,
                                           "Enter the width of the board :", 3, 12)
        self.spinboxJ = self.createSpinbox(True,
                                           "Number of player :", 2, 8)
        self.spinboxB = self.createSpinbox(False,
                                           "Number of bots :", 1, 7)
        self.savebutton()
        self.loadbutton()

        self.canvas.bind('<Button-1>', self.placePawn)
        btn = tk.Button(self.root, text="New board", font=("Arial", 15),
                        command=self.nvplateau)
        btn.pack()

        style = ttk.Style()
        style.configure("MyCheckbutton.TCheckbutton", font=("Arial", 15))
        ttk.Checkbutton(self.root,
                        style="MyCheckbutton.TCheckbutton",
                        text='Do you want bots ?',
                        command=self.botornot,
                        variable=self.agreement,
                        onvalue='Bot added',
                        offvalue='Bot removed'
                        ).pack()

    def initializeCanvas(self):
        self.rectangles = []
        self.image_container = []
        for i in range(self.grid.getHeight()):
            self.rectangles.append([])
            self.image_container.append([])

            for j in range(self.grid.getWidth()):
                x0 = j * 40
                y0 = i * 40
                x1 = x0 + 40
                y1 = y0 + 40
                xi = (x1-x0)/2+x0
                yi = (y1-y0)/2+y0
                self.rectangles[i].append(self.canvas.create_rectangle(
                    x0, y0, x1, y1, outline=self.grid.getCurrentPlayer(), width=2))
                self.image_container[i].append(
                    self.canvas.create_image(xi, yi, image=self.casePNG[0]))

        for i, row in enumerate(self.grid.getGrid()):
            for j, cell in enumerate(row):
                self.canvas.itemconfig(
                    self.rectangles[i][j], fill=cell.getPlayer().getColor())

    def update(self):
        for i, row in enumerate(self.grid.getGrid()):
            for j, cell in enumerate(row):
                if cell.getPawnNumber() < 4:
                    score_case = cell.getPawnNumber()
                else:
                    score_case = 3
                self.canvas.itemconfig(
                    self.image_container[i][j], image=self.casePNG[score_case])

                print("\n"*10, self.grid.getCurrentPlayer(),
                      self.grid.getNextPlayer())
                self.canvas.itemconfig(
                    self.rectangles[i][j],
                    outline=self.grid.getNextPlayer().getColor(),
                    fill=cell.getPlayer().getColor()
                )

    def placePawn(self, event):

        x, y = event.x, event.y
        selectedRow = y // 40
        selectedCol = x // 40

        if self.grid.checkWin():
            return

        if isinstance(self.grid.getCurrentPlayer(), game.Bot):
            coordo = self.grid.getCurrentPlayer().pickCoordo(self.grid)
            while self.grid.placePawn(coordo, self.grid.getCurrentPlayer()) == False:
                coordo = self.grid.getCurrentPlayer().pickCoordo(self.grid)
        else:
            if self.grid.placePawn((selectedRow, selectedCol), self.grid.getCurrentPlayer()) == False:
                return
        self.grid.expandPawn((selectedRow, selectedCol),
                             self.grid.getCurrentPlayer())

        # self.grid.display()
        self.update()
        self.grid.NextPlayer()

        if self.grid.checkWin():
            self.root.after(1, self.displayWinner)

    def displayWinner(self):
        winner = self.grid.getPlayerList()[0].getNumber()
        messagebox.showinfo("Winner", f"The winner is {winner}")

    def clear(self):
        for i, row in enumerate(self.grid.getGrid()):
            for j, cell in enumerate(row):
                self.canvas.delete(self.rectangles[i][j])
                self.canvas.delete(self.image_container[i][j])

    def nvplateau(self):
        messagebox.showinfo("Board update", "The board has been updated")
        height = int(self.spinbox1.get())
        width = int(self.spinbox2.get())
        nbPlayer = int(self.spinboxJ.get())
        bots = self.botornot()
        nbBots = int(self.spinboxB.get())

        self.clear()
        self.grid = game.createGame(width, height, nbPlayer, bots, nbBots)
        self.initializeCanvas()
        self.canvas.configure(width=self.grid.getWidth()
                              * 40, height=self.grid.getHeight()*40)
        self.canvas.configure(outline=self.grid.getCurrentPlayer().getColor())
        self.canvas.pack()
        self.update()

    def createSpinbox(self, state: bool, text: str, min: int, max: int):
        label = tk.Label(self.root, text=text)
        label.config(font="Arial")
        label.pack()
        spinbox = tk.Spinbox(self.root, from_=min, to=max)
        spinbox.pack()
        if state:
            spinbox.config(validate="key", validatecommand=(
                spinbox.register(self.validation), "%P"))
        else:
            spinbox.config(state='disabled', validate="key", validatecommand=(
                spinbox.register(self.validation), "%P"))
        spinbox.bind("<Key>", self.ignore_input)
        return spinbox

    def botornot(self):
        tk.messagebox.showinfo(title='Result', message=self.agreement.get())
        if self.agreement.get() == 'Bot added':
            self.spinboxB.config(state='normal')
            return True
        else:
            self.spinboxB.config(state='disabled')
            return False

    def validation(self, new_text):
        if new_text.isdigit():
            return True
        elif new_text == "":
            return True
        else:
            return False

    def ignore_input(self, event):
        return "break"

    def savebutton(self):
        save_button = tk.Button(
            self.root, text="Save game", command=self.saveGame)
        save_button.config(font=("Arial", 15))
        save_button.pack()

    def loadbutton(self):
        load_button = tk.Button(
            self.root, text="Load game", command=self.loadGame)
        load_button.config(font=("Arial", 15))
        load_button.pack()

    def saveGame(self):
        self.grid.saveGame()
        # self.grid.display()

    def loadGame(self):
        self.grid.loadGame()
        # self.grid.display()
        self.initializeCanvas()
        self.update()


if __name__ == "__main__":
    GI = GraphicalInterfaces()
    GI.root.mainloop()
