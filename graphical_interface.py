import main as main
import tkinter as tk
from tkinter import PhotoImage, ttk, messagebox



grid = main.createGame()

root = tk.Tk()
root.geometry('1500x750')
root.title('Expansion')

agreement = tk.StringVar()

casev= PhotoImage(file="image/casevide.png")
unpion= PhotoImage(file="image/unpion.png")
deuxpion= PhotoImage(file="image/deuxpion.png")
troispion= PhotoImage(file="image/troispion.png")
case = [casev,unpion,deuxpion,troispion]

canvas = tk.Canvas(root, width=grid.getWidth()*40, height=grid.getHeight()*40)
canvas.pack()


rectangles = []
image_container = []
curentPlayer = 0
for i in range(grid.getHeight()):
    rectangles.append([])
    image_container.append([])
canvas = tk.Canvas(root, width=grid.getWidth()*40, height=grid.getHeight()*40)
canvas.pack()

rectangles = []
curentPlayer = 0

for i in range(grid.getHeight()):
    rectangles.append([])

    for j in range(grid.getWidth()):
        x0 = j * 40
        y0 = i * 40
        x1 = x0 + 40
        y1 = y0 + 40
        xi = (x1-x0)/2+x0
        yi = (y1-y0)/2+y0
        rectangles[i].append(canvas.create_rectangle(
            x0, y0, x1, y1, outline=grid.getPlayerList()[curentPlayer], width=2))
        image_container[i].append(canvas.create_image(xi,yi,image=case[0]))
        rectangles[i].append(canvas.create_rectangle(
            x0, y0, x1, y1, outline=grid.getPlayerList()[curentPlayer], width=2))


for i, row in enumerate(grid.getGrid()):
    for j, cell in enumerate(row):
        canvas.itemconfig(
            rectangles[i][j], fill=cell.getPlayer().getColor())


def placePawn(event):
    global curentPlayer

    x, y = event.x, event.y
    selectedRow = y // 40
    selectedCol = x // 40

    if grid.checkWin():
        return 

    if isinstance(grid.getPlayerList()[curentPlayer], main.Bot):
        coordo = grid.getPlayerList()[curentPlayer].pickCoordo(grid)
        while grid.placePawn(coordo, grid.getPlayerList()[curentPlayer]) == False:
            coordo = grid.getPlayerList()[curentPlayer].pickCoordo(grid)
    else:
        if grid.placePawn((selectedRow, selectedCol), grid.getPlayerList()[curentPlayer]) == False:
            return
    grid.expandPawn((selectedRow, selectedCol),
                    grid.getPlayerList()[curentPlayer])

    update()

    if curentPlayer < len(grid.getPlayerList())-1:
        curentPlayer += 1
    else:
        curentPlayer = 0


def update():
    # print(grid.getGrid())
    for i, row in enumerate(grid.getGrid()):
        for j, cell in enumerate(row):
            score_case = cell.getPawnNumber()
            canvas.itemconfig(image_container[i][j], image=case[score_case])
            if curentPlayer < len(grid.getPlayerList())-1:
                canvas.itemconfig(
                    rectangles[i][j],
                    outline=grid.getPlayerList()[curentPlayer+1],
                    fill=cell.getPlayer().getColor()
                )
                

            else:
                canvas.itemconfig(
                    rectangles[i][j],
                    outline=grid.getPlayerList()[0],
                    fill=cell.getPlayer().getColor()
                )






def validation(new_text):
    if new_text.isdigit():
        return True
    elif new_text == "":
        return True
    else:
        return False

def ignore_input(event):
    return "break"

label = tk.Label(root, text="Entre la longueur du plateau :")
label.pack()
spinbox1 = tk.Spinbox(root, from_=3, to=10)
spinbox1.pack()
spinbox1.config(validate="key", validatecommand=(spinbox1.register(validation), "%P"))
spinbox1.bind("<Key>", ignore_input)

label = tk.Label(root, text="Entrez la largeur du plateau :")
label.pack()
spinbox2 = tk.Spinbox(root, from_=3, to=12)
spinbox2.pack()
spinbox2.config(validate="key", validatecommand=(spinbox2.register(validation), "%P"))
spinbox2.bind("<Key>", ignore_input)

label = tk.Label(root, text="Nombres de joueurs :")
label.pack()
spinboxJ = tk.Spinbox(root, from_=2, to=8)
spinboxJ.pack()
spinboxJ.config(validate="key", validatecommand=(spinboxJ.register(validation), "%P"))
spinboxJ.bind("<Key>", ignore_input)


def botornot():
    tk.messagebox.showinfo(title='Result', message=agreement.get())
    if agreement.get() == 'Ajout de bots':
        spinboxB.config(state='normal')
    else:
        spinboxB.config(state='disabled')

ttk.Checkbutton(root,
                text='Voulez vous jouer avec des bots ?',
                command=botornot,
                variable=agreement,
                onvalue='Ajout de bots', 
                offvalue='Retrait des bots'
                ).pack()

label = tk.Label(root, text="Nombres de Bots :")
label.pack()
spinboxB = tk.Spinbox(root, from_=1, to=7)
spinboxB.pack()
spinboxB.config(state='disabled', validate="key", validatecommand=(spinboxJ.register(validation), "%P"))
spinboxB.bind("<Key>", ignore_input)

def nvplateau():
    messagebox.showinfo("Mise à jour", "Mise à jour du plateau")
    h = int(spinbox1.get())
    w = int(spinbox2.get())
    nvplateau(w, h)



btn = tk.Button(root, text = "Nouveau Plateau", command = nvplateau)
btn.pack()










canvas.bind('<Button-1>', placePawn)


root.mainloop()
