#importer les bibliothèques
from PIL import Image, ImageTk
from tkinter import Label
from matplotlib import cm
from matplotlib.pyplot import subplots, tight_layout, savefig
from data import color_bg1
from tkinter import Tk,Label

def afficher_Image(fen,row,column,name,size,Images):
    #Retourne une image png
    #Il faut donner en entrée la fenêtre,row,column,name,size,le nom qu'on veut donner à l'image

    if name[-4:] != '.png':
        name += '.png'
    Images += [ImageTk.PhotoImage(Image.open(name).resize(size))]
    imgLabel = Label(fen, image = Images[-1], background=color_bg1)
    imgLabel.grid(row=row, column=column)
    fen.update()
    return Images