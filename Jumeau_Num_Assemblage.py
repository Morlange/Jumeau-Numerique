from tkinter import Label, Tk
from PIL import ImageTk, Image

fen = Tk()
fen.title("Jumeau numérique Assemblage")


image = ImageTk.PhotoImage(Image.open("Ah....png"))
TempLabel = Label(fen, image=image)
TempLabel.pack()


fen.mainloop()