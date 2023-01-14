import main as main
import tkinter as tk
from tkinter import PhotoImage, ttk, messagebox


class GraphicalInterfaces():
    def __init__(self):
        self.grid = main.createGame(12, 10, 2, False)
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=self.grid.getWidth() *
                                40, height=self.grid.getHeight()*40)
        self.agreement = tk.StringVar()
        self.rectangles = []
        self.image_container = []
        self.curentPlayer = 0
        self.casePNG = [PhotoImage(file="./image/noHole.png"),
                        PhotoImage(file="./image/singleHole.png"),
                        PhotoImage(file="./image/twoHoles.png"),
                        PhotoImage(file="./image/threeHoles.png")]

        self.root.geometry('1500x750')
        self.root.title('Expansion')
        self.canvas.pack()
        self.initializeCanvas()

        self.spinbox1 = self.createSpinbox(True,
                                           "Entre la longueur du plateau :", 3, 10)
        self.spinbox2 = self.createSpinbox(True,
                                           "Entrez la largeur du plateau :", 3, 12)
        self.spinboxJ = self.createSpinbox(True,
                                           "Nombres de joueurs :", 2, 8)
        self.spinboxB = self.createSpinbox(False,
                                           "Nombres de Bots :", 1, 7)

        self.canvas.bind('<Button-1>', self.placePawn)
        btn = tk.Button(self.root, text="Nouveau Plateau",
                        command=self.nvplateau)
        btn.pack()

        ttk.Checkbutton(self.root,
                        text='Voulez vous jouer avec des bots ?',
                        command=self.botornot,
                        variable=self.agreement,
                        onvalue='Ajout de bots',
                        offvalue='Retrait des bots'
                        ).pack()

    def initializeCanvas(self):
        self.rectangles = []
        self.image_container = []
        self.curentPlayer = 0
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
                    x0, y0, x1, y1, outline=self.grid.getPlayerList()[self.curentPlayer], width=2))
                self.image_container[i].append(
                    self.canvas.create_image(xi, yi, image=self.casePNG[0]))

        for i, row in enumerate(self.grid.getGrid()):
            for j, cell in enumerate(row):
                self.canvas.itemconfig(
                    self.rectangles[i][j], fill=cell.getPlayer().getColor())

    def update(self):
        # print(self.grid.getGrid())
        for i, row in enumerate(self.grid.getGrid()):
            for j, cell in enumerate(row):
                if cell.getPawnNumber() < 4:
                    score_case = cell.getPawnNumber()
                else:
                    score_case = 3
                self.canvas.itemconfig(
                    self.image_container[i][j], image=self.casePNG[score_case])

                if self.curentPlayer < len(self.grid.getPlayerList())-1:
                    self.canvas.itemconfig(
                        self.rectangles[i][j],
                        outline=self.grid.getPlayerList()[self.curentPlayer+1],
                        fill=cell.getPlayer().getColor()
                    )
                else:
                    self.canvas.itemconfig(
                        self.rectangles[i][j],
                        outline=self.grid.getPlayerList()[0],
                        fill=cell.getPlayer().getColor()
                    )

    def placePawn(self, event):

        x, y = event.x, event.y
        selectedRow = y // 40
        selectedCol = x // 40

        if self.grid.checkWin():
            return

        if isinstance(self.grid.getPlayerList()[self.curentPlayer], main.Bot):
            coordo = self.grid.getPlayerList(
            )[self.curentPlayer].pickCoordo(self.grid)
            while self.grid.placePawn(coordo, self.grid.getPlayerList()[self.curentPlayer]) == False:
                coordo = self.grid.getPlayerList(
                )[self.curentPlayer].pickCoordo(self.grid)
        else:
            if self.grid.placePawn((selectedRow, selectedCol), self.grid.getPlayerList()[self.curentPlayer]) == False:
                return
        self.grid.expandPawn((selectedRow, selectedCol),
                             self.grid.getPlayerList()[self.curentPlayer])

        self.update()

        if self.curentPlayer < len(self.grid.getPlayerList())-1:
            self.curentPlayer += 1
        else:
            self.curentPlayer = 0

    def clear(self):
        for i, row in enumerate(self.grid.getGrid()):
            for j, cell in enumerate(row):
                self.canvas.delete(self.rectangles[i][j])
                self.canvas.delete(self.image_container[i][j])

    def nvplateau(self):
        messagebox.showinfo("Mise à jour", "Mise à jour du plateau")
        height = int(self.spinbox1.get())
        width = int(self.spinbox2.get())
        nbPlayer = int(self.spinboxJ.get())
        nbBots = int(self.spinboxB.get())
        self.clear()
        # TODO: Change False if Bots is checked
        self.grid = main.createGame(width, height, nbPlayer, False, nbBots)
        self.initializeCanvas()
        self.update()

    def createSpinbox(self, state: bool, text: str, min: int, max: int):
        label = tk.Label(self.root, text=text)
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
        if self.agreement.get() == 'Ajout de bots':
            self.spinboxB.config(state='normal')
        else:
            self.spinboxB.config(state='disabled')

    def validation(self, new_text):
        if new_text.isdigit():
            return True
        elif new_text == "":
            return True
        else:
            return False

    def ignore_input(self, event):
        return "break"


if __name__ == "__main__":
    GI = GraphicalInterfaces()
    GI.root.mainloop()
