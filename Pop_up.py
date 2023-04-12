from tkinter import Tk, Label
from PIL import ImageTk, Image
from data import color_bg1
import image

image_info = Image.open("info.png").resize((50,50))
#https://icones8.fr/icons/set/warning
#img = ImageTk.PhotoImage(image=image_info)
#message = "Hello world"

def main(message,image_info):
    fen_pop = Tk()
    fen_pop.title("Informations")
    Message = Label(fen_pop,text=message)
    imgage_info_tk = ImageTk.PhotoImage(image=image_info)
    Image_info = Label(fen_pop,image=imgage_info_tk, background=color_bg1)
    Image_info.grid(row = 0, column=0)
    Message.grid(row = 0, column = 1)
    fen_pop.mainloop()
    return imgage_info_tk

if __name__ == "__main__":
    main("Hello world",image_info)