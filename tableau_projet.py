import tkinter as tk


root = tk.Tk()

canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

rectangles = []
colors = []
playercolor = ["BLACK","RED","ORANGE","YELLOW","GREEN","BLUE","PURPLE","PINK","TEAL"]
c = 1

for i in range(10):
    rectangles.append([])
    colors.append([])
    for j in range(10):
        x0 = j * 40
        y0 = i * 40
        x1 = x0 + 40
        y1 = y0 + 40
        rectangles[i].append(canvas.create_rectangle(x0, y0, x1, y1, outline=playercolor[c], width=2))
        colors[i].append('white')

def change_color(event):
  global c
  
  x, y = event.x, event.y
  row = y // 40
  col = x // 40
  rectangle = rectangles[row][col]

  if colors[row][col] == 'white':
    canvas.itemconfig(rectangle, fill='red')
    colors[row][col] = 'red'
    c=c+1
  else:
    canvas.itemconfig(rectangle, fill='white')
    colors[row][col] = 'white'
    c=c+1

  for i in range(10):
    for j in range(10):
      rectangle = rectangles[i][j]
      canvas.itemconfig(rectangle, outline=playercolor[c], width=2)
    
  if c == 8:
    c = 0

canvas.bind('<Button-1>', change_color)

root.mainloop()
