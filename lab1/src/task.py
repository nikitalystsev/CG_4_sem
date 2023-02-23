from tkinter import Canvas, Tk

root = Tk()

canvas = Canvas(root, width=500, height=500)
canvas.pack()

canvas.create_line(0, 0, 0, 100, width=5)

root.mainloop()
