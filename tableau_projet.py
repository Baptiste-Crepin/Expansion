from tkinter import *
import tkinter

root = Tk()
frame=Frame(root)
Grid.rowconfigure(root, 0, weight=1)
Grid.columnconfigure(root, 0, weight=1)
frame.grid(row=0, column=0, sticky=N+S+E+W)
grid=Frame(frame)
grid.grid(sticky=N+S+E+W, column=0, row=7, columnspan=2)
Grid.rowconfigure(frame, 7, weight=1)
Grid.columnconfigure(frame, 0, weight=1)

active="grey"
defaut="white"

def main(height,width):
  for x in range(width):
    for y in range(height):
      btn = tkinter.Button(frame, bg=defaut)
      btn.grid(column=x, row=y, sticky=N+S+E+W)
      btn["command"] = lambda btn=btn: click(btn)

  for x in range(width):
    Grid.columnconfigure(frame, x, weight=1)

  for y in range(height):
    Grid.rowconfigure(frame, y, weight=1)

  return frame

def click(button):
  if(button["bg"] == active):
    button["bg"] = defaut
  else:
    button["bg"] = active

w= main(5,5)
tkinter.mainloop()