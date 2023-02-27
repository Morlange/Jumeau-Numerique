from PIL import Image, ImageTk
from tkinter import Label

def afficher_Image(fen,row,column,name,size,Images):
    Images += [ImageTk.PhotoImage(Image.open(name).resize(size))]
    imgLabel = Label(fen, image = Images[-1])
    imgLabel.grid(row=row, column=column)
    fen.update()
    return Images