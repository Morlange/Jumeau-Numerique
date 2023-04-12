from PIL import Image, ImageTk
from tkinter import Tk

def main(mot):
    if mot == "info":
        image_info = Image.open("info.png").resize((50,50))
        img = ImageTk.PhotoImage(image=image_info)
        return img
    if mot == "warning":
        image_warning = Image.open("warning.png").resize((50,50))
        img = ImageTk.PhotoImage(image=image_warning)
        return img
