from PIL import Image, ImageTk
from tkinter import Label, Tk, Canvas, Menu, Entry, N, S, VERTICAL, LabelFrame, Button
from tkinter import ttk
from tkinter.messagebox import showinfo
import xlrd
import xlsxwriter
import subprocess
from matplotlib import cm
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Wedge, Rectangle
import time
from data import LogoAM, nb_produits, liste_produit, OF, color_bg1, color_bg, color_fg
from opcua import Client



def main():
    global LogoAM
    url = "opc.tcp://127.0.0.1:4880"
    client = Client(url)
    client.connect()
    print("Client connected")

    NbPiecesMachines = client.get_node("ns = 2; i = 3")

    


    def flux ():
        # creation de l'objet fenetre
        fen_flux= Tk()

        #Titre de la fenetre
        fen_flux.title('Analyse de production')

        #Taille de la fenetre
        fen_flux.geometry('1300x630')

        #icone de fenetre
        fen_flux.iconbitmap('logo-AM.ico')

        #configuration du fond
        fen_flux.config(background='#D3D3D3')
        
        label_titre = Label(fen_flux, text='Analyse de production', height=1,fg='black',font=('Calibri', 14),bg='#D3D3D3') 
        label_titre.grid(row=0,column=1)

        #Frame TRS
        frame_TRS = LabelFrame(fen_flux, text='TRS', font =('Calibri', 12), bg='#D3D3D3', labelanchor='nw')
        frame_TRS.grid(row=1,column=0)
        Label(frame_TRS, text='Flux').grid(row=1, column=0)

        #def afficher_Image(fen,row,column,name,size):
        """
        size = (100,150)
        img = ImageTk.PhotoImage(Image.open("flux.png").resize((50,50)))
        canv = Canvas(frame_TRS, highlightthickness = 0, bg="#333333", height=size[0], width=size[1])
        canv.grid(row=0, column=0)
        canv.create_image(0,0, image = img)"""
        image = ImageTk.PhotoImage(Image.open("flux.png"))
        TempLabel = Label(fen_flux, image=image)
        TempLabel.grid(row=0,column=0) 
        
        #Création de la Combobox
        listeCombo = ttk.Combobox(fen_flux, values=liste_produit)
            
        #Choisir l'élément qui s'affiche par défaut
        listeCombo.grid(row=0, column=2,padx=0,pady=10)


        def action(event):
            select = listeCombo.get()

            affichage= NbPiecesMachines.get_value()
            print(affichage)
            #Liste_machines=["Four", "Coulée","Usinage","Assemblage"]
            coordonnées_machines=[[100,100],[200,200],[200,100],[100,200]]
            label_nbpiece = [None for i in range(len(affichage))]
            for i in range (len(affichage)):
                label_nbpiece[i] = Label(fen_flux,text=affichage[i],height=1,font=('Calibri',14),fg=color_bg, bg='transparentcolor')
                label_nbpiece[i].place(x=coordonnées_machines[i][0], y=coordonnées_machines[i][1])
                print('action lancée')


        listeCombo.bind("<<ComboboxSelected>>", action) 
    
        fen_flux.mainloop()



    

    flux()
main()