import tkinter

canvas_width = 500
canvas_height = 500

root = tkinter.Tk()
canvas = tkinter.Canvas(root, height=canvas_height, width=canvas_width, background="black")
canvas.pack()

s = canvas.create_oval(100, 100, 400, 400, fill="white")

canvas.moveto(s, 250 - 150, 250 - 150)


root.mainloop()