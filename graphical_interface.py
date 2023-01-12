import main as main
import tkinter as tk


grid = main.createGame()

root = tk.Tk()
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


canvas.bind('<Button-1>', placePawn)


root.mainloop()
