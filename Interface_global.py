# coding: utf-8

# import bibliothèque
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
from data import client,LogoAM,TRS,Images_TRS,Temps_de_production,Nombre_pieces,color_bg1,color_bg,color_fg



def ouvrir_analyse ():
    subprocess.Popen("python3 analyse.py")
    subprocess.Popen("python3 analyse2.py")
    

def ouvrir_OF ():
    subprocess.Popen("python3 ouvrir_OF.py")


def ouvrir_etat ():
    print(Serveur_ON)
    if Serveur_ON:
        subprocess.Popen("python3 Interface_machines.py")
    else :
        # creation de l'objet fenetre
        fen_Error_co= Tk()

        #Titre de la fenetre
        fen_Error_co.title('Erreur de connection')

        #Taille de la fenetre
        fen_Error_co.geometry('300x200')

        #icone de fenetre
        fen_Error_co.iconbitmap(LogoAM)

        #configuration du fond
        fen_Error_co.config(background=color_bg1)
        #Ajout d'un titre 
        label_titre = Label(fen_Error_co, text='Erreur de connection \nVeuillez lancer le serveur en premier', height=2,font=('Calibri', 14),fg=color_fg, bg = color_bg1) 
        label_titre.grid(row=0,column=0, padx=10, pady=75)

        fen_Error_co.mainloop()

def lancer_serveur():

    global Serveur_ON
    if not Serveur_ON:
        subprocess.Popen("python3 Serveur.py")
        time.sleep(2)
        client.connect()
        print("Interface connectée")
        Serveur_ON = True
        label_etat_serv.configure(text="Etat du serveur : Connecté")
        fen.update()

def stop_serveur():
#On restart le programme pour espérer arrêter le serveur
    global Serveur_ON
    if Serveur_ON :
        Stop = client.get_node("ns = 2; i = 16")
        Stop.set_value(1)
        client.disconnect()
        Serveur_ON = False
        label_etat_serv.configure(text="Etat du serveur : Déconnecté")
        fen.update()

def quitter():
    if Serveur_ON :
        stop_serveur()
    fen.destroy()

def flux():
    subprocess.Popen("python3 flux.py")

def ouvrir_jum_ass():
    subprocess.Popen("python3 Jumeau_Num_Assemblage.py")

    
#Creation de l'objet fenetre
fen= Tk()

#Titre de la fenetre
fen.title('Gestion de production')

#Taille de la fenetre
fen.geometry('1300x630')

#icone de fenetre
fen.iconbitmap(LogoAM)

#configuration du fond
fen.config(background=color_bg1)

#Menu
mon_menu=Menu(fen)
fen.config(menu=mon_menu)

#Les 4 principaux onglets
mon_menu.add_command(label='Etat',command=ouvrir_etat)
mon_menu.add_command(label='OF',command=ouvrir_OF)
mon_menu.add_command(label='Analyse',command=ouvrir_analyse)

# boutons fenetre
bouton_etat = Button (fen, text = 'Etat des machines',bd=1, font=('Calibri', 12),fg=color_fg, bg = color_bg,command=ouvrir_etat)
bouton_etat.grid(row=1, column=0, padx=40, pady=100)

bouton_flux =  Button (fen,text='Affichage du flux', bd=1, font=('Calibri', 12),fg=color_fg, bg = color_bg,command=flux)
bouton_flux.grid(row=3, column=1, padx=40,pady=100)

bouton_OF =  Button (fen, text = 'Ordres de fabrication',bd=1,font=('Calibri', 12), fg=color_fg, bg = color_bg,command=ouvrir_OF)
bouton_OF.grid(row=1, column=1, padx=40, pady=100)

bouton_analyse =  Button (fen, text = 'Analyse de production',bd=1,font=('Calibri', 12), fg=color_fg, bg = color_bg,command=ouvrir_analyse)
bouton_analyse.grid(row=1, column=2, padx=40, pady=100)

bouton_jumeau_assemblage =  Button (fen, text = 'Jumeau Numérique Assemblage',bd=1,font=('Calibri', 12), fg=color_fg, bg = color_bg,command=ouvrir_jum_ass)
bouton_jumeau_assemblage.grid(row=1, column=3, padx=40, pady=100)

bouton_start_server =  Button (fen, text = 'Lancer le serveur',bd=1,font=('Calibri', 12), fg=color_fg, bg = color_bg,command=lancer_serveur)
bouton_start_server.grid(row=2, column=1, padx=40, pady=100)


bouton_serv =  Button (fen, text = 'Stopper le serveur',bd=1,font=('Calibri', 12), fg=color_fg, bg = color_bg,command=stop_serveur)
bouton_serv.grid(row=2, column=2, padx=40, pady=100)

label_etat_serv = Label(fen, text='Etat du serveur : Déconnecté', height=2,font=('Calibri', 14),fg=color_fg, bg = color_bg1)
label_etat_serv.grid(row=2, column=0, padx=40, pady=100)

bouton_quitter =  Button (fen, text = 'Quitter',bd=1,font=('Calibri', 12), fg=color_fg, bg = color_bg,command=quitter)
bouton_quitter.grid(row=3, column=0, padx=40, pady=40)


#Boucle d'affichage
fen.mainloop()



# ajouter un bouton "ajouter un ordre de fabrication" : voir le bug 
#modifier le produit

